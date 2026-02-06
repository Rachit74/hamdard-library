from rest_framework.viewsets import ModelViewSet
from library.models import File
from .serializers import FileSerializer

class FileViewSet(ModelViewSet):
    """
    API endpoint that allows files to be viewed or edited.
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    http_method_names = ["get"]
