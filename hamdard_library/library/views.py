from django.shortcuts import render, redirect, get_object_or_404
from .models import File
from .forms import FileUploadForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import hashlib
from django.conf import settings
from django.urls import reverse
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.http import HttpResponseNotFound
from django_ratelimit.decorators import ratelimit


# file hash function
def hash_uploaded_file(uploaded_file, chunk_size=8192):
    hasher = hashlib.sha256()
    for chunk in uploaded_file.chunks(chunk_size):
        hasher.update(chunk)

    return hasher.hexdigest()

# home view
def home(request):
    files = File.objects.filter(file_status=True).order_by('-uploaded_at')[:5]
    unapproved_files = File.objects.filter(file_status=False).count()
    context = {
        'files':files,
        'unapproved_files': unapproved_files,
    }
    return render(request, 'library/home.html', context=context)

# deparments view
def departments(request):
    return render(request, 'library/departments.html')

@ratelimit(key='ip', rate='5/m')
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = request.FILES['file_path']

            # hash
            file_hash = hash_uploaded_file(uploaded_file)
            uploaded_file.seek(0)

            # block dublicates
            if File.objects.filter(file_hash=file_hash).exists():
                messages.error(request, "This file already exists.")
                return redirect('home')

            # save
            new_file = form.save(commit=False)
            new_file.file_hash = file_hash

            if request.user.is_authenticated:
                new_file.uploaded_by = request.user

            new_file.save()

            messages.success(request, "File uploaded!")
            return redirect('home')

    else:
        form = FileUploadForm()

    return render(request, 'library/upload_file.html', {'form': form})

#file approval page

@login_required
def file_approve_requests(request):
    user = request.user
    if not user.is_staff:
        messages.info(request, "You do not have access!")
        return redirect('home')
    
    unapproved_files = File.objects.filter(file_status=False)
    return render(request, 'library/requests.html', {'unapproved_files': unapproved_files})

@login_required
def approve_file(request, file_id):
    user = request.user
    if not user.is_staff:
        messages.info(request, "You do not have access!")
        return redirect('home')
    
    file = get_object_or_404(File, id=file_id)
    if file:
        file.file_status = True
        file.save()
        messages.success(request, "File Approved!")
        return redirect('approval-requests')
    
# departments/<department> page

def department(request,department_):
    department_ = department_.upper()
    department_list = ['SEST', 'SAHSR', 'HIMSER', 'SUMER', 'SCLS', 'SPER', 'SNSAH', 'SIST', 'SMBS', 'SHSS', 'LAW']
    if department_ in department_list:
        search_query = request.GET.get('search', '')
        filter_status = request.GET.get('filter', 'all')
        sem_filter = request.GET.get('sem', 'all')
        # Check if the sem_filter is a digit before converting
        if sem_filter.isdigit():
            sem_filter = int(sem_filter)
        else:
            sem_filter = 'all'

        user = request.user
        
        if filter_status == 'approved':
            files = File.objects.filter(file_department=department_, file_status=True).order_by('-uploaded_at')
        elif filter_status == 'unapproved':
            files = File.objects.filter(file_department=department_, file_status=False).order_by('-uploaded_at')
        elif type(sem_filter) == int:
            files = File.objects.filter(file_department=department_, semester=sem_filter).order_by('-uploaded_at')
        else:
            files = File.objects.filter(file_department=department_).order_by('-uploaded_at')

        if search_query:
            files = files.filter(file_name__icontains=search_query)

        paginator = Paginator(files, 9)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context = {
            'page_object':page_object,
            'department': department_,
            'search_query':search_query,
            'user':user
        }
        return render(request, 'library/department.html', context)
    else:
        return HttpResponseNotFound(f"Department {department_} not found!")

#delete file
@login_required
def delete_file(request, file_id):
# Retrieve the file object
    file = get_object_or_404(File, id=file_id)
    user = request.user

    # Correct permission check
    if not user.is_staff and not user.is_superuser and file.uploaded_by != user:
        messages.warning(request, "You cannot delete this file!")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    else:        
        file.delete()

        messages.success(request, "File Deleted!")
        return redirect(request.META.get('HTTP_REFERER', '/'))

"""
Info Views
These views just render informational templates like donate page, API Docs and Developers / Contribution Page
No application logic is controlled by these views
"""

def donate(request):
    return render(request, 'library/donate.html')

def api_docs(request):
    return render(request, 'library/api_docs.html')

def developers(request):
    return render(request, 'library/for-developers.html')