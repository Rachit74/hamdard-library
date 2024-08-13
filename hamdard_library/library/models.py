from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#file post Model

class File(models.Model):
        # File name field
        file_name = models.CharField(max_length=255)
        
        # File department field
        file_department = models.CharField(max_length=255)
        
        # File path field (auto-handled by Django's FileField)
        file_path = models.FileField(upload_to='uploads/')

        #file approve status
        file_status = models.BooleanField(default=False)
        
        # ForeignKey linking to the User who uploaded the file
        uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
        
        # Timestamp of when the file was uploaded
        uploaded_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.file_name