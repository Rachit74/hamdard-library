from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegistartionForm(UserCreationForm):
    first_name = forms.CharField(label="Display Name:", max_length=250, required=False)

    usable_password = None

    class Meta:
        model = User
        fields = ['username', 'first_name', 'password1', 'password2']

    
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput)