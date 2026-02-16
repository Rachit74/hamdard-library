from django.urls import path
from .views import create_file, get_files, delete_file, get_unapproved_files, approve_file

from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("files/", csrf_exempt(get_files)),
    path("files/create/", csrf_exempt(create_file)),
    path("files/delete/<uuid:id>/", csrf_exempt(delete_file)),

    # path("files/unapproved/", get_unapproved_files),
    # path("files/approve/<uuid:id>/", approve_file)
]
