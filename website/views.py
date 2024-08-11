from flask import Blueprint, render_template, request, redirect, url_for, flash
import os
from . import db
from .admin import admin_
from .models import User
import firebase_admin
from firebase_admin import storage, firestore
import uuid



views = Blueprint('views', __name__)

db = firestore.client()
bucket = storage.bucket()

# file compress
# def compress_pdf(pdf_document):
#     # Create an in-memory bytes buffer for the compressed PDF
#     compressed_file_in_memory = io.BytesIO()

#     # Save the document to the buffer with compression
#     pdf_document.save(compressed_file_in_memory, garbage=4, deflate=True)
#     compressed_file_in_memory.seek(0)

#     return compressed_file_in_memory


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
                filename = title
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

    files = []
    for doc in docs:
        file_metadata = doc.to_dict()
        file_name = file_metadata.get('file_name')
        file_path = file_metadata.get('file_path')
        file_status = file_metadata.get('file_status')
        file_department = file_metadata.get('file_department')
        
        # Generate public URL for each file
        blob = bucket.blob(file_path)
        file_url = blob.public_url

        files.append({
            'file_name': file_name,
            'file_path': file_path,
            'file_url': file_url,
            'file_status': file_status,
            'file_department': file_department,
            'department': file_metadata.get('file_department'),
            'id': doc.id,
        })

    return render_template('files.html', files=files, department=department)