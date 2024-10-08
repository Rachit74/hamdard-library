from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='library_home'),
    path("upload_file/", views.upload_file, name='library_upload_file'),
    path("departments/", views.departments, name='library_departments'),
    path("approve_requests/", views.file_approve_requests, name='library_approve_requests'),
    path("approve_file/<int:file_id>", views.approve_file, name='library_approve_file'),
    path("department/<str:department_>", views.department, name='library_department'),
    path("delete_file/<int:file_id>", views.delete_file, name='library_delete_file'),
    path("upvote_file/<int:file_id>", views.upvote, name='library_upvote_file'),
    path("downvote_file/<int:file_id>", views.downvote, name='library_downvote_file'),
    path("donate/", views.donate, name='library_donate'),
]