from django.shortcuts import render, redirect, get_object_or_404
from .models import File
from .forms import FileUploadForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.urls import reverse

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
            return redirect(reverse('library_department', args=[new_file.file_department]))

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
    
# departments/<department> page

def department(request,department_):
    search_query = request.GET.get('search', '')
    filter_status = request.GET.get('filter', 'all')
    
    if filter_status == 'approved':
        files = File.objects.filter(file_department=department_, file_status=True)
    elif filter_status == 'unapproved':
        files = File.objects.filter(file_department=department_, file_status=False)
    else:
        files = File.objects.filter(file_department=department_)

    if search_query:
        files = files.filter(file_name__icontains=search_query)


    return render(request, 'library/department.html', {'files':files, 'department': department_, 'search_query':search_query})

#delete file
def delete_file(request, file_id):
# Retrieve the file object
    file = get_object_or_404(File, id=file_id)
    user = request.user

    # Correct permission check
    if not user.is_staff and not user.is_superuser and file.uploaded_by != user:
        messages.warning(request, "You cannot delete this file!")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    # Remove file from physical storage
    file_path = os.path.join(settings.MEDIA_ROOT, str(file.file_path))
    if os.path.exists(file_path):
        os.remove(file_path)

    # Delete the file record from the database
    file.delete()

    messages.success(request, "File Deleted!")
    return redirect(request.META.get('HTTP_REFERER', '/'))