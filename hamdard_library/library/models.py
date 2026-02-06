from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import uuid

# Create your models here.

#file post Model

class File(models.Model):
        id = models.UUIDField(
              primary_key=True,
              default=uuid.uuid4,
              editable=False
        )

        file_name = models.CharField(max_length=255)
        
        file_department = models.CharField(max_length=255)
        
        # File path field (auto-handled by Django's FileField)
        file_path = models.FileField(upload_to='uploads/')

        #file approve status
        file_status = models.BooleanField(default=False)
        
        # ForeignKey linking to the User who uploaded the file
        uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
        
        # Timestamp of when the file was uploaded
        uploaded_at = models.DateTimeField(auto_now_add=True)

        # Downloads
        downloads = models.IntegerField(default=0)

        #semester file belongs to
        semester = models.IntegerField(default=1)

        #file hash
        file_hash = models.CharField(max_length=64, unique=True)

        def __str__(self):
            return self.file_name
         