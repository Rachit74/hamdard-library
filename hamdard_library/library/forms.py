# forms.py
from django import forms
from .models import File
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegistartionForm(UserCreationForm):
    username = forms.CharField(max_length=200, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username = username).exists():
            raise forms.ValidationError("This Username is already taken!")
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Removing password-based authentication
        if 'usable_password' in self.fields:
            del self.fields['usable_password']
    
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput)


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file_name', 'file_department', 'file_path']  # Fields to be displayed in the form
