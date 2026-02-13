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
            "uploaded_by",
        ]


class FileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [
            "file_name",
            "file_path",
            "file_department",
            "semester",
        ]