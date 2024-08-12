from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from .forms import FileUploadForm, UserLoginForm, RegistartionForm
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

# home view
def home(request):
    return render(request, 'library/home.html')

# deparments view
def departments(request):
    return render(request, 'library/departments.html')

# file upload view
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form but don't commit to the database yet
            new_file = form.save(commit=False)
            # Assign the current logged-in user to the uploaded_by field
            new_file.uploaded_by = request.user
            # Now commit the form to the database
            new_file.save()
            return render(request, 'library/home.html')
    else:
        form = FileUploadForm()
    
    return render(request, 'library/upload_file.html', {'form': form})


#login view
def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('library_home')
    else:
        form = UserLoginForm()
    return render(request, 'library/login.html', {'form': form})

#registation view
def register_user(request):
    if request.method == 'POST':
            form = RegistartionForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, "User Registration Successful!")
                return redirect('library_home')  # Redirect to a homepage or another view
            else:
                print(form.errors)
    else:
        form = RegistartionForm()
    return render(request, 'library/register.html', {'form':form})

#logut user
def logout_user(request):
    logout(request)
    messages.success(request,"Logged out!")
    return redirect('library_login_user')

# fake user meta data

#individual user route
def user_profile(request):
    current_user = request.user
    user = current_user
    print(user.username)
    return render(request, 'library/user_profile.html', {"user" : user})