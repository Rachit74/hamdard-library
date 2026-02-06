from rest_framework import serializers
from library.models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [
            "id",
            "file_name",
            "file_department",
            "file_path",
            "semester",
        ]
