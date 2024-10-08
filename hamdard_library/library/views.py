from django.shortcuts import render, redirect, get_object_or_404
from .models import File, Upvote, Downvote
from .forms import FileUploadForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.urls import reverse
from django.core.paginator import Paginator

from django.http import HttpResponseNotFound

from .vote_check import has_upvoted, has_downvoted

# Create your views here.

# home view
def home(request):
    files = File.objects.filter(file_status=True).order_by('-uploaded_at')[:5]
    return render(request, 'library/home.html', {'files':files})

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
            print(new_file.file_path)

            # generate and set a file identifier to the current uploaded file
            new_file.file_identifier = f"{new_file.file_path}_identifier"
            print(new_file.file_identifier)

            new_file.uploaded_by = request.user

            # checks if the file with the current file identifier exiists in any of the record
            check_for_file = File.objects.filter(file_identifier=new_file.file_identifier).exists()


            # if file exists then __pass__
            if check_for_file:
                """
                if a file with the file_identifier exists then we will set the file_path of current file
                to the file_path of the file that already exists in the storage.
                """
                dublicate_file = File.objects.filter(file_identifier=new_file.file_identifier).first()
                print("File with the current identifier exists, can't upload dublicate files!")
                new_file.file_path = dublicate_file.file_path
                new_file.save()
                messages.success(request, f"File Uploaded!")

            else:
                """
                if a file with the file_identifier does not exists then we will upload the file to database
                """
                new_file.save()
                messages.success(request, f"File Uploaded!")

            return redirect('library_user_profile')

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

"""
using .order_by('-upvotes') to sort the files in decending order by number of upvotes they have
"""
def department(request,department_):
    department_ = department_.upper()
    department_list = ['SEST', 'HIMSER', 'SUMER', 'SCLS', 'SPER', 'SNSAH', 'SIST', 'SMBS', 'SHSS', 'LAW']
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
            files = File.objects.filter(file_department=department_, file_status=True).order_by('-votes_ratio')
        elif filter_status == 'unapproved':
            files = File.objects.filter(file_department=department_, file_status=False).order_by('-votes_ratio')
        elif type(sem_filter) == int:
            files = File.objects.filter(file_department=department_, semester=sem_filter).order_by('-votes_ratio')
        else:
            files = File.objects.filter(file_department=department_).order_by('-votes_ratio')

        if search_query:
            files = files.filter(file_name__icontains=search_query).order_by('-votes_ratio')

        paginator = Paginator(files, 6)
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
        #file identifier of the current file (/delete_file/id)
        current_file_identifier = file.file_identifier

        #check if files with the current identifier exists

        check_for_file = File.objects.filter(file_identifier = current_file_identifier).count()

        """
        if more than one file with current_file_identifier exists
        """
        if check_for_file>1:
            """
            deletes the file data but does not remove the file from the physical storage
            """
            file.delete()
        else:
            """
            Removes the file from physical storage if no file with the current_file_identifier exists
            """
            file_path = os.path.join(settings.MEDIA_ROOT, str(file.file_path))
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Delete the file record from the database
            file.delete()

        messages.success(request, "File Deleted!")
        return redirect(request.META.get('HTTP_REFERER', '/'))

#file upvote view
"""
view to handle file upvotes
Users can upvote a file but can not upvote their own file
A user can upvote a file only once
"""

@login_required
def upvote(request, file_id):
    user = request.user
    file = get_object_or_404(File, id=file_id)

    if not file.file_status:
        messages.success(request, "File must be approved to perform operations")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    """
    checks if the combination of user and file exists in the Upvote model
    if not then allows the user to upvote the file and saved the combination
    if yes then raise error.
    """
    if not Upvote.objects.filter(user=user, file=file):
        has_downvoted(user,file)
        file.upvotes += 1
        file.votes_ratio = file.upvotes-file.downvotes
        file.save()
        upvote = Upvote.objects.create(user=user, file=file)
        upvote.save()
        messages.success(request, "Upvoted!")
        print(file.upvotes)
    else:
        messages.success(request,"Can not upvote again")

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def downvote(request, file_id):
    user = request.user
    file = get_object_or_404(File, id=file_id)

    if not file.file_status:
        messages.success(request, "File must be approved to perform operations")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    if not Downvote.objects.filter(user=user, file=file):
        has_upvoted(user,file)
        file.downvotes += 1
        file.votes_ratio = file.upvotes-file.downvotes
        file.save()
        downvote = Downvote.objects.create(user=user,file=file)
        downvote.save()
        messages.success(request, "Downvoted :(")
        print(file.upvotes)
    else:
        messages.success(request,"Can not downvote again")

    return redirect(request.META.get('HTTP_REFERER', '/'))

def donate(request):
    return render(request, 'library/donate.html')