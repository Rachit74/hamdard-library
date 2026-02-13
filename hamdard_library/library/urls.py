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

    path("donate/", views.donate, name="donate"),

    # api docs disabled for now
    # path("api_docs/", views.api_docs, name="api-docs")
]