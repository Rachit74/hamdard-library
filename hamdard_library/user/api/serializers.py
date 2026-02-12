from rest_framework import serializers
from django.contrib.auth.models import User

# User login serializer
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
