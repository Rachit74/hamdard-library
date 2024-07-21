from flask import Blueprint, render_template, request, send_from_directory, redirect,url_for
from werkzeug.utils import secure_filename
import os
from . import UPLOAD_FOLDER
from . import db
from .models import File

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/upload', methods=['GET','POST'])
def upload():
    if request.method == "POST":
        file = request.files['file']
        title = request.form['title']
        dept = request.form['dept']

        if file and title and dept:
            filename = secure_filename(file.filename)
            file_path = os.path.join('./static', 'uploads')
            file.save(file_path)
            
            new_file = File(file_name=title, file_path=filename, dept=dept)
            db.session.add(new_file)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('upload.html')