from flask import Blueprint, render_template, request, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from . import db
from .admin import admin_
from .models import User
from flask_login import login_required,login_user,current_user,logout_user,login_manager
from werkzeug.security import generate_password_hash
import firebase_admin
from firebase_admin import storage, credentials, firestore
import uuid



views = Blueprint('views', __name__)

db = firestore.client()
bucket = storage.bucket()

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == "POST":
        file = request.files['file']
        title = request.form['title']
        dept = request.form['dept']

        if file and title and dept:
            filename = secure_filename(file.filename)
            blob = bucket.blob(filename)
            blob.upload_from_file(file)
            blob.make_public()  # Make the file publicly accessible

            doc_id = str(uuid.uuid4())

            file_metadata = {
                'file_name': filename,
                'file_title': title,
                'file_department': dept,
                'file_status': "false",
                'url': blob.public_url,
                'file_path': filename  # Ensure this is stored for generating URLs later
            }
            db.collection('file_metadata').document(doc_id).set(file_metadata)

            flash("File Uploaded!")
            return redirect(url_for('views.home'))
    return render_template('upload.html')

@views.route('/departments')
def departments():
    return render_template('departments.html')

@views.route('/departments/<department>')
def department(department):
    # Fetch files metadata from Firestore
    files_ref = db.collection('file_metadata').where('file_department', '==', department.upper())
    docs = files_ref.stream()

    files_with_urls = []
    for doc in docs:
        file_metadata = doc.to_dict()
        file_name = file_metadata.get('file_name')
        file_path = file_metadata.get('file_path')
        file_status = file_metadata.get('file_status')
        
        # Generate public URL for each file
        blob = bucket.blob(file_path)
        file_url = blob.public_url

        files_with_urls.append({
            'file_name': file_name,
            'file_path': file_path,
            'file_url': file_url,
            'file_status': file_status,
            'department': file_metadata.get('file_department'),
            'id': doc.id,
        })

    return render_template('files.html', files=files_with_urls, department=department)