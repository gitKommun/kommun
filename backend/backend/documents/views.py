from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Folder
from .serializers import FolderSerializer

class FolderListAPIView(APIView):
    def get(self, request, IDcommunity):
        folders = Folder.objects.filter(community=IDcommunity)
        serializer = FolderSerializer(folders, many=True)
        return Response(serializer.data)
    
class FolderCreateAPIView(APIView):
    def post(self, request, IDcommunity):
        data = request.data.copy()
        data['community'] = IDcommunity
        serializer = FolderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class FolderDetailAPIView(APIView):
    def get(self, request, IDcommunity, IDfolder):
        folder = get_object_or_404(Folder, pk=IDfolder, community=IDcommunity) 
        serializer = FolderSerializer(folder)
        return Response(serializer.data)

    def put(self, request, IDcommunity, IDfolder):
        folder = get_object_or_404(Folder, pk=IDfolder, community=IDcommunity) 
        serializer = FolderSerializer(folder, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, IDcommunity, IDfolder):
        folder = get_object_or_404(Folder, pk=IDfolder, community=IDcommunity)
        folder.delete()
        return Response(status=204)
    

