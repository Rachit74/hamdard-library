from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError

from .serializers import FileCreateSerializer, FileSerializer
from library.models import File


# get all approved files
@api_view(['GET'])
def get_files(request):
    # Filter files that are approved by the admin
    files = File.objects.filter(file_status=True)
    serializer = FileSerializer(files, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

# create file view
@api_view(['POST'])
@permission_classes([AllowAny])
def create_file(request):
    serializer = FileCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        file_obj = serializer.save(
            uploaded_by=request.user if request.user.is_authenticated else None
        )

        return Response(
            {
                "message": "File uploaded successfully",
                "id": file_obj.id
            },
            status=status.HTTP_201_CREATED
        )
    except IntegrityError:
        return Response({'message': "File Already Exists"}, status=status.HTTP_400_BAD_REQUEST)

# delete file
"""
Admins can delete file
file owner can delete file
"""
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_file(request, id):
    file = File.objects.get(id=id)

    if not (request.user.is_staff or file.uploaded_by == request.user):
        return Response(
            {"error": "Permission denied"},
            status=status.HTTP_403_FORBIDDEN
        )

    file.delete()
    return Response(
        {"message": "File deleted"},
        status=status.HTTP_204_NO_CONTENT
    )


# get unapproved files
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unapproved_files(request):
    files = File.objects.filter(file_status=False)
    serializer = FileSerializer(files, many=True)

    return Response(serializer.data)

# approve file
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_file(request, id):
    file = File.objects.get(id=id)

    user = request.user

    if not user.is_staff:
        return Response(
            {"Error": "Permission Denied"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    file.file_status = True
    file.save()
    return Response(
        {"message": "File Approved!"},
        status=status.HTTP_200_OK
    )