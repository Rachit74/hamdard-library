from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("upload/", views.upload_file, name="upload-file"),
    path("departments/", views.departments, name="departments"),
    path("approval/", views.file_approve_requests, name="approval-requests"),

    path("approve/<uuid:file_id>/", views.approve_file, name="approve-file"),
    path("delete/<uuid:file_id>/", views.delete_file, name="delete-file"),

    path("department/<str:department_>/", views.department, name="department"),


    # url for informational views
    path("donate/", views.donate, name="donate"),
    path("developers/api_docs/", views.api_docs, name="api-docs"),
    path("developers/", views.developers, name="for-developers"),
    path("developers/contribute/", views.contribution, name="contribution"),
]