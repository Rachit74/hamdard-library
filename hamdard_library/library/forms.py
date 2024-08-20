# forms.py
from django import forms
from .models import File

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file_name', 'file_department', 'file_path', 'semester']  # Fields to be displayed in the form
