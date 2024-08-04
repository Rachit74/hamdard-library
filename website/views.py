from flask import Blueprint, render_template, request, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from . import UPLOAD_FOLDER
from . import db
from .admin import admin_
from .models import File, User
from flask_login import login_required,login_user,current_user,logout_user,login_manager
from werkzeug.security import generate_password_hash

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

                       #   ADMIN ROUTES   #
# --------------------------------------------------------------------------------------------#

# # login route
# @admin_.route('/login', methods=["POST","GET"])
# def login():
#     if request.method == "POST":
#         email = request.form['email']
#         password = request.form['password']

#         user = User.query.filter_by(email=email).first()

#         if user.password == password:
#             login_user(user,remember=True)
#             flash("Logged in!")
#             return redirect(url_for('admin_.file_requests'))
#         else:
#             flash("Wrong Password")

#     return render_template('login.html')

# # admin logout route
# @login_required
# @admin_.route('/logout')
# def logout():
#     logout_user()
#     flash("Admin Logged Out!")
#     return redirect(url_for('views.home'))

# # basic admin route which just redirects to files approval requests (later will add admin dashboard)
# @login_required
# @admin_.route('/')
# def admin():
#         if not current_user.is_authenticated:
#             flash("You do not have the permissions!")
#             return redirect(url_for('views.home'))
#         return redirect(url_for('admin_.file_requests'))

# #admin signup route (used to create more admins)
# # Only a currently logged in admin can create more admins
# @login_required
# @admin_.route('/signup', methods=["POST","GET"])
# def signup():
#     if not current_user.is_authenticated:
#             flash("You do not have the permissions!")
#             return redirect(url_for('views.home'))

#     if request.method == "POST":
#         username = request.form.get('username')
#         email = request.form.get('email')
#         password = request.form.get('password')

#         if not username or not email or not password:
#             flash("All fields are required.")
#             return redirect(url_for('admin_.signup'))

#         # Check if the user already exists
#         existing_user = User.query.filter_by(email=email).first()
#         if existing_user:
#             flash("User with this email already exists.")
#             return redirect(url_for('admin_.signup'))

#         # Create and add new admin user
#         password_hash = generate_password_hash(password)
#         user = User(username=username, email=email, password=password_hash, user_admin=True)
#         db.session.add(user)
#         db.session.commit()
#         flash("New Admin Account Created!")
#         return redirect(url_for('admin_.file_requests'))

#     return render_template("signup.html")

# # file request functions
# @login_required
# @admin_.route('/requests')
# def file_requests():
#     if not current_user.is_authenticated:
#             flash("You do not have the permissions!")
#             return redirect(url_for('views.home'))
#     files=File.query.all()
#     return render_template('request.html', files=files)

# #file approve route (file id is passed into the route from the template)
# # changes the status of the file to approved
# @login_required
# @admin_.route('/file_approve/<int:file_id>')
# def file_approve(file_id):
#     if not current_user.is_authenticated:
#             flash("You do not have the permissions!")
#             return redirect(url_for('views.home'))
#     file = File.query.get(file_id)

#     if file:
#         file.file_status = True

#         db.session.commit()
#         flash("File Approved")
#     else:
#         flash("File Not Found")
    
#     return redirect(url_for('admin_.file_requests'))

# #admin dashbaord
# @login_required
# @admin_.route('/admin_dashboard')
# def admin_dashboard():
#     if not current_user.is_authenticated:
#         flash("You do not have access")
#         return redirect(url_for('views.home'))
    
#     admin = User.query.get(current_user.get_id())
#     return render_template("dashboard.html", admin=admin)

# #view for all admins page
# #can only be accessed by super admin (to be added soon)
# @admin_.route('/admons')
# def admons():
#      if not current_user.is_authenticated:
#           flash("You do not have access!")
#           return redirect(url_for('views.home'))
#      admins = User.query.all()
#      return render_template("admons.html", admins=admins)

# #delete admin route
# @admin_.route("/delete_admin/<int:aid>")
# def delete_admin(aid):
#     if not current_user.is_authenticated:
#         flash("You do not have access!")
#         return redirect(url_for('views.home'))
#     admin = User.query.get(aid)
#     db.session.delete(admin)
#     db.session.commit()

#     if current_user.get_id() == aid:
#          logout_user
#          flash("Admin Deleted")
#          return redirect(url_for('views.home'))
    
#     flash("Admin was deleted")
#     return redirect(url_for('admin_.admin_dashboard'))

# #delete file functions (gets the file id as form html template)
# @login_required
# @admin_.route('/delete_file/<int:file_id>')
# def delete_file(file_id):
#     if not current_user.is_authenticated:
#             flash("You do not have the permissions!")
#             return redirect(url_for('views.home'))
#     file = File.query.get(file_id)

#     if file:
#         # Construct the file path
#         file_path = os.path.join(UPLOAD_FOLDER, file.file_path)

#         # Delete the file record from the database
#         db.session.delete(file)
#         db.session.commit()

#     # Remove the file from the file system
#     if os.path.isfile(file_path):
#         os.remove(file_path)

#         flash("File successfully deleted!")
#     else:
#         flash("File not found!")

#     return redirect(url_for('admin_.file_requests'))