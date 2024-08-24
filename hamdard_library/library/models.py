from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

#file post Model

class File(models.Model):
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

        # File Identifier to prevent dublicate uploads
        file_identifier = models.CharField(max_length=100, default="")

        # Number of upvotes a file has
        upvotes = models.IntegerField(default=0)

        # Number of downvotes a file has
        downvotes = models.IntegerField(default=0)

        # upvote to download ration
        votes_ratio = models.IntegerField(default=0)

        #semester file belongs to
        semester = models.IntegerField(default=1)

        def __str__(self):
            return self.file_name
        
"""
Upvote model which has one to one relationship with the user model as well as the file model to make sure that a
user can upvote a particular post only once.

This model will store the record of user_id and file_id for each file that a particular user will upvote
when ever the upvote function will be called it will check the Upvote table (model) if the user_id had
alredy upvoted the file_id.
"""
class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    """
    class meta used to control the meta data options of the model
    """
    class Meta:
        """
        makes sure that one particular user can only upvote a file once

        user refrences the user which upvoted the file
        file refrences the file that was upvoted

        unique_together makes sure that a user can only upvote a file once, if a combination of user and
        file already exists in the database then error will be raised
        """
        unique_together = ('user', 'file') 
    
    def __str__(self):
        return f"{self.user.username} upvoted {self.file.file_name}"
    
"""
Downvote model with same logic as the upvote model
"""
class Downvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'file')

    def __str__(self) -> str:
         return f"{self.user.username} downvoted {self.file.file_name}"
         