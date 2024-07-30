from flask import Blueprint, render_template, request, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from . import UPLOAD_FOLDER
from . import db
from .models import File

views = Blueprint('views', __name__)

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
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            new_file = File(file_name=title, file_path=filename, dept=dept)
            db.session.add(new_file)
            db.session.commit()
            flash("File Uploaded!")
            return redirect(url_for('views.home'))  # Changed 'index' to 'views.home'
    return render_template('upload.html')

@views.route('/departments')
def departments():
    return render_template('departments.html')

@views.route('/departments/<department>')
def department(department):
    files = File.query.filter_by(dept=department.upper()).all()
    return render_template('files.html', files=files, department=department)

@views.route('/requests')
def file_requests():
    files=File.query.all()
    return render_template('request.html', files=files)

@views.route('/file_approve/<int:file_id>')
def file_approve(file_id):
    file = File.query.get(file_id)

    if file:
        file.file_status = True

        db.session.commit()
        flash("File Approved")
    else:
        flash("File Not Found")
    
    return redirect(url_for('views.file_requests'))