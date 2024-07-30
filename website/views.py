from flask import Blueprint, render_template, request, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from . import UPLOAD_FOLDER
from . import db
from .models import File, User
from flask_login import login_required,login_user,current_user,logout_user,login_manager
from werkzeug.security import generate_password_hash

views = Blueprint('views', __name__)
admin_ = Blueprint('admin_', __name__)

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



#admin routes

@admin_.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user.password == password:
            login_user(user,remember=True)
            flash("Logged in!")
            return redirect(url_for('admin_.file_requests'))
        else:
            flash("Wrong Password")

    return render_template('login.html')

@login_required
@admin_.route('/')
def admin():
        return redirect(url_for('admin_.file_requests'))

# file request functions
@login_required
@admin_.route('/requests')
def file_requests():
    files=File.query.all()
    return render_template('request.html', files=files)

@login_required
@admin_.route('/file_approve/<int:file_id>')
def file_approve(file_id):
    file = File.query.get(file_id)

    if file:
        file.file_status = True

        db.session.commit()
        flash("File Approved")
    else:
        flash("File Not Found")
    
    return redirect(url_for('admin.file_requests'))

@login_required
@admin_.route('/logout')
def logout():
    logout_user()
    flash("Admin Logged Out!")
    return redirect(url_for('views.home'))

@login_required
@admin_.route('/signup', methods=["POST","GET"])
def signup():
    if not current_user.user_admin:
            flash("You do not have the permissions!")
            return redirect(url_for('views.home'))

    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash("All fields are required.")
            return redirect(url_for('admin_.signup'))

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("User with this email already exists.")
            return redirect(url_for('admin_.signup'))

        # Create and add new admin user
        password_hash = generate_password_hash(password)
        user = User(username=username, email=email, password=password_hash, user_admin=True)
        db.session.add(user)
        db.session.commit()
        flash("New Admin Account Created!")
        return redirect(url_for('admin_.file_requests'))

    return render_template("signup.html")