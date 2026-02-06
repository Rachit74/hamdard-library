from rest_framework.viewsets import ModelViewSet
from library.models import File
from .serializers import FileSerializer

class FileViewSet(ModelViewSet):
    """
    API endpoint that allows files to be viewed or edited.
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer

    def get_queryset(self):
        queryset = File.objects.filter(file_status=True)

        filename = self.request.query_params.get("filename")
        if filename:
            queryset = queryset.filter(file_name__icontains=filename)

        return queryset
