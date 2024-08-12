from django.shortcuts import render, redirect
from .models import User, File
from .forms import FileUploadForm, UserLoginForm, RegistartionForm
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
            messages.success(request, "File Uploaded!")
            return render(request, 'library/home.html')
    else:
        form = FileUploadForm()
    
    return render(request, 'library/upload_file.html', {'form': form})

#file approval page

@login_required
def file_approve_requests(request):
    user = request.user
    if not user.is_staff:
        messages.info(request, "You do not have access!")
        return redirect('library_home')
    
    unapproved_files = File.objects.filter(file_status=False)
    return render(request, 'library/requests.html', {'unapproved_files': unapproved_files})

@login_required
def approve_file(request, file_id):
    user = request.user
    if not user.is_staff:
        messages.info(request, "You do not have access!")
        return redirect('library_home')
    
    file = File.objects.filter(id=file_id).first()
    if file:
        file.file_status = True
        file.save()
        messages.success(request, "File Approved!")
        return redirect('library_approve_requests')