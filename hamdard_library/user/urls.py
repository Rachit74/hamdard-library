from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_user, name='login'),
    path("register/", views.register_user, name='register'),
    path("profile/", views.user_profile, name='profile'),
    path("logout/", views.logout_user, name='logout'),
    path("delete_account/", views.delete_user, name='delete-account'),
]