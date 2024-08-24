from django.contrib.auth.models import User
from .models import File, Upvote, Downvote

def has_upvoted(user, file):
    if Upvote.objects.filter(user=user, file=file).exists():
        upvote_to_be_removed = Upvote.objects.get(user=user, file=file)
        upvote_to_be_removed.delete()
        file.upvotes -= 1
        file.save()

def has_downvoted(user, file):
    if Downvote.objects.filter(user=user, file=file).exists():
        downvote_to_be_removed = Downvote.objects.get(user=user, file=file)
        downvote_to_be_removed.delete()
        file.downvotes -= 1
        file.save()