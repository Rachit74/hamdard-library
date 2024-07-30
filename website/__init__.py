from flask import Flask, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from os import path,makedirs
import os
from os.path import join, dirname, realpath
from .key import key
from flask_login import LoginManager,current_user,login_manager
from functools import wraps

# from flask_migrate import Migrate


db = SQLAlchemy()
DB_NAME = "database.db"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = key
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    db.init_app(app)


    '''
    checks if the /static/upload folder exists, if not then creates one
    solved my issue of "file not found" when uploading
    '''
    if not path.exists(UPLOAD_FOLDER):
        makedirs(UPLOAD_FOLDER)
    
    from .views import views
    from .views import admin_

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(admin_, url_prefix='/admin')

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "admin_.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        from .models import User
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Created database!")