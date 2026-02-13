from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError

from .serializers import FileCreateSerializer, FileSerializer
from library.models import File


# get all files
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

