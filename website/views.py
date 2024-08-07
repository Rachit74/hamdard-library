from flask import Blueprint, render_template, request, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from . import UPLOAD_FOLDER
from . import db
from .admin import admin_
from .models import File, User
from flask_login import login_required,login_user,current_user,logout_user,login_manager
from werkzeug.security import generate_password_hash
import firebase_admin
from firebase_admin import storage


views = Blueprint('views', __name__)

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
            
            # Store metadata in the local database
            new_file = File(file_name=title, file_path=filename, dept=dept)
            db.session.add(new_file)
            db.session.commit()
            flash("File Uploaded!")
            return redirect(url_for('views.home'))
    return render_template('upload.html')

@views.route('/departments')
def departments():
    return render_template('departments.html')

@views.route('/departments/<department>')
def department(department):
    # Fetch files metadata from local database
    files = File.query.filter_by(dept=department.upper()).all()

    # Generate public URLs for each file stored in Firebase Storage
    files_with_urls = []
    for file in files:
        blob = bucket.blob(file.file_path)
        file_url = blob.public_url
        files_with_urls.append({
            'file_name': file.file_name,
            'file_path': file.file_path,
            'file_url': file_url,
            'department': file.dept,
            'id': file.id,
        })

    return render_template('files.html', files=files_with_urls, department=department)