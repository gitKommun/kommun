from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Folder, Document
from .serializers import FolderSerializer, FolderListCompleteSerializer, DocumentUploadSerializer, DocumentSerializer, FolderDetailSerializer

class FolderListAPIView(APIView):
    def get(self, request, IDcommunity):
        folders = Folder.objects.filter(community=IDcommunity).annotate(document_count=Count('documents'))
        serializer = FolderListCompleteSerializer(folders, many=True)
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
    
class FolderOpenAPIView(APIView):
    def get(self, request, IDcommunity, IDfolder):
        folder = get_object_or_404(Folder, pk=IDfolder, community_id=IDcommunity)
        serializer = FolderDetailSerializer(folder)
        return Response(serializer.data)

class DocumentUploadAPIView(APIView):
    def post(self, request, IDcommunity, IDfolder):
        #folder = get_object_or_404(Folder, pk=IDfolder, community_id=IDcommunity)
        data = request.data.copy()
        data['community'] = IDcommunity
        data['folder'] = IDfolder

        serializer = DocumentUploadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DocumentDetailAPIView(APIView):
    def get(self, request, IDdocument, IDcommunity):
        document = get_object_or_404(Document, pk=IDdocument)
        serializer = DocumentSerializer(document)
        return Response(serializer.data)

class DocumentDeleteAPIView(APIView):
    def delete(self, request, IDdocument, IDcommunity):
        document = get_object_or_404(Document, pk=IDdocument)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DocumentDownloadAPIView(APIView):
    def get(self, request, IDcommunity, IDdocument):
        document = get_object_or_404(Document, pk=IDdocument, community_id=IDcommunity)
        file_handle = document.file.open()
        response = FileResponse(file_handle, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
        return response