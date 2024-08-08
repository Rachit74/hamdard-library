from flask import Flask, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from os import path,makedirs
import os
from os.path import join, dirname, realpath
from .key import key
from flask_login import LoginManager,current_user,login_manager
from functools import wraps
import firebase_admin
from firebase_admin import credentials, storage, firestore

# fire base creds
# Initialize Firebase Admin SDK
cred = credentials.Certificate('./cred.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'hamdardlibrarydb.appspot.com'
})

db = firestore.client()
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg',}

def create_app():
    app = Flask(__name__,static_folder='website/static', template_folder='website/templates')
    app.config['SECRET_KEY'] = key

    
    from .views import views
    from .admin import admin_

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(admin_, url_prefix='/admin')


    login_manager = LoginManager()
    login_manager.login_view = "views.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.get_user(user_id)

    return app