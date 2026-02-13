from django.urls import path
from .views import create_file, get_files

urlpatterns = [
    path("files/", get_files),
    path("files/create/", create_file),
]
