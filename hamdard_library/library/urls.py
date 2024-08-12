from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='library_home'),
    path("upload_file/", views.upload_file, name='library_upload_file'),
    path("departments/", views.departments, name='library_departments'),
    path("login/", views.login_user, name='library_login_user'),
    path("register/", views.register_user, name='library_register_user'),
    path("user_profile/", views.user_profile, name='library_user_profile'),
    path("user_logut/", views.logout_user, name='library_logout_user'),
]