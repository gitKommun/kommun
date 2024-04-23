from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Folder
from .serializers import FolderSerializer

class FolderListAPIView(APIView):
    def get(self, request):
        folders = Folder.objects.all()
        serializer = FolderSerializer(folders, many=True)
        return Response(serializer.data)
    
class FolderCreateAPIView(APIView):
    def post(self, request):
        serializer = FolderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

