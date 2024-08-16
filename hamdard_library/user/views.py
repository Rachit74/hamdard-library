from django.shortcuts import render, redirect
from .forms import UserLoginForm, RegistartionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from library.models import File
# Create your views here.


#login view
def login_user(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            #checks of username and password for that username in the db
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('library_home')
    else:
        form = UserLoginForm()
    return render(request, 'user/login.html', {'form': form})

#registation view
def register_user(request):
    if request.method == 'POST':
        form = RegistartionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #checks if both the passwords are same
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            messages.success(request, "User Registration Successful!")
            return redirect('library_home')  # Redirect to a safe page
        else:
            messages.warning(request, "Please correct the errors below.")
            print(form.errors)
    else:
        form = RegistartionForm()
    return render(request, 'user/register.html', {'form':form})

#logut user (logs the user out)
def logout_user(request):
    logout(request)
    messages.success(request,"Logged out!")
    return redirect('library_login_user')

# fake user meta data

#individual user Profile route
"""
Gets the current user and the files uploaded by that user and sends response based on that information
"""
@login_required
def user_profile(request):
    current_user = request.user
    user = current_user
    filter_option = request.GET.get('filter', 'all')

    #gets the files based on filter passed in html (approved, unapproved or all files)
    if filter_option == 'approved':
        user_files = File.objects.filter(uploaded_by=current_user, file_status=True)
    elif filter_option == 'unapproved':
        user_files = File.objects.filter(uploaded_by=current_user, file_status=False)
    else:
        user_files = File.objects.filter(uploaded_by=current_user)

    # counting the number of file uploads a user has
    uploads=0
    for i in user_files:
        uploads += 1

    return render(request, 'user/user_profile.html', {"user" : user, "user_files": user_files, "uploads": uploads})

#delete user function
"""
Gets the current user and deletes it from the database
"""
@login_required
def delete_user(request):
    #gets current user
    user = request.user

    #delets the user
    user.delete()

    #flashes the message of user being deleted
    messages.warning(request, "User Deleted!")

    #redirects to login page after the user is deleted
    return redirect('library_login_user')