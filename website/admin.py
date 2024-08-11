from flask import Blueprint, render_template, request, send_from_directory, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from . import db
from .models import User
from flask_login import login_required,login_user,current_user,logout_user,login_manager
from werkzeug.security import generate_password_hash
import firebase_admin
from firebase_admin import storage, credentials, firestore
import uuid


admin_ = Blueprint('admin_', __name__)

db = firestore.client()
bucket = storage.bucket()


                       #   ADMIN ROUTES   #
# --------------------------------------------------------------------------------------------#

@admin_.route('/register', methods=['GET', 'POST'])
def register():
    if not current_user.is_authenticated:
        flash("You do not have permissions")
        return redirect(url_for('views.home'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        is_admin = True
        is_super_admin = False

        user_id = str(uuid.uuid4())
        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'is_admin': is_admin,
            'is_super_admin': is_super_admin,
        }
        db.collection('users').document(user_id).set(user_data)
        flash('Registration successful!')
        return redirect(url_for('admin_.login'))

    return render_template('signup.html')

@admin_.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users_ref = db.collection('users').where('email', '==', email).limit(1).stream()
        for doc in users_ref:
            user_data = doc.to_dict()
            user = User(doc.id, user_data['username'], user_data['email'], user_data['password'], user_data['is_admin'], user_data['is_super_admin'])
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('views.home'))
        flash('Invalid email or password')
    return render_template('login.html')

@admin_.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('admin_.login'))

@login_required
@admin_.route('/')
def admin():
        if not current_user.is_authenticated:
            flash("You do not have the permissions!")
            return redirect(url_for('views.home'))
        return redirect(url_for('admin_.file_requests'))

# file request functions
@login_required
@admin_.route('/requests')
def file_requests():
    if not current_user.is_authenticated:
            flash("You do not have the permissions!")
            return redirect(url_for('views.home'))
    
    file_ref = db.collection('file_metadata')
    docs = file_ref.stream()

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
    return render_template('request.html', files=files)

#file approve route (file id is passed into the route from the template)
# changes the status of the file to approved
@login_required
@admin_.route('/file_approve/<file_id>')
def file_approve(file_id):
    if not current_user.is_authenticated:
        flash("You do not have the permissions!")
        return redirect(url_for('views.home'))
    
    file_ref = db.collection('file_metadata').document(file_id)
    file_ref.update({'file_status': 'true'})
    flash("File approved!")
    return redirect(url_for('admin_.file_requests'))


#admin dashbaord
@login_required
@admin_.route('/admin_dashboard')
def admin_dashboard():
    if not current_user.is_authenticated:
        flash("You do not have access")
        return redirect(url_for('views.home'))
    
    admin = db.collection('users').document(current_user.get_id())
    doc = admin.get()

    # if not doc.exists():
    #     flash("Admin not found")
    #     return redirect(url_for('views.home'))

    admin_data = doc.to_dict()

    admin_details = {
        'id': doc.id,
        'username': admin_data.get('username'),
        'email': admin_data.get('email'),
        'is_super_admin': admin_data.get('is_super_admin'),
        'is_admin': admin_data.get('is_admin'),
    }


    return render_template("dashboard.html", admin=admin_details)

#view for all admins page
#can only be accessed by super admin (to be added soon)
@admin_.route('/admons')
@login_required
def admons():
    if not current_user.is_authenticated:
        flash("You do not have the permissions!")
        return redirect(url_for('views.home'))
    if not current_user.is_super_admin:
        flash("You do not have the permissions!")
        return redirect(url_for('views.home'))

    # Fetch all users who are admins
    admins_ref = db.collection('users').where('is_admin', '==', True)
    admins_docs = admins_ref.stream()
    
    admins = []
    for doc in admins_docs:
        admin_data = doc.to_dict()
        admins.append({
            'id': doc.id,
            'username': admin_data['username'],
            'email': admin_data['email'],
            'is_super_admin': admin_data['is_super_admin']
        })

    return render_template('admons.html', admins=admins)

#delete admin route
@admin_.route("/delete_admin/<aid>")
def delete_admin(aid):
    if not current_user.is_authenticated:
        flash("You do not have access!")
        return redirect(url_for('views.home'))
    if not current_user.is_super_admin():
         flash("You cannot delete other admins! [IS NOT SUPER ADMIN]")
         return redirect(url_for('admin_.admons'))
         
    _admin = db.collection('users').document(aid)
    _admin.delete()

    if current_user.get_id() == aid:
         logout_user
         flash("Admin Deleted")
         return redirect(url_for('views.home'))
    
    flash("Admin was deleted")
    return redirect(url_for('admin_.admin_dashboard'))

#delete file functions (gets the file id as form html template)
@login_required
@admin_.route('/delete_file/<file_id>')
def delete_file(file_id):
    if not current_user.is_authenticated:
        flash("You do not have the permissions!")
        return redirect(url_for('views.home'))
    
    file_ref = db.collection('file_metadata').document(file_id)
    file_metadata = file_ref.get().to_dict()

    if file_metadata:
        file_path = file_metadata.get('file_path')
        
        # Delete the blob from Firebase Storage
        blob = bucket.blob(file_path)
        blob.delete()

        # Delete the document from Firestore
        file_ref.delete()
        
        flash("File deleted successfully!")
    else:
        flash("File not found!")

    return redirect(url_for('admin_.file_requests'))