from django.urls import path
from . import views

urlpatterns = [
    path("api_docs/", views.api_docs, name="api-docs"),
    path("", views.developers, name="for-developers"),
]