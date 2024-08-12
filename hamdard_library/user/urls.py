from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_user, name='library_login_user'),
    path("register/", views.register_user, name='library_register_user'),
    path("user_profile/", views.user_profile, name='library_user_profile'),
    path("user_logut/", views.logout_user, name='library_logout_user'),
    path("delete_account/", views.delete_user, name='library_delete_account'),
]