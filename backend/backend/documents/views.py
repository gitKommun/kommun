from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Folder, Document
from .serializers import FolderSerializer, FolderListCompleteSerializer, DocumentUploadSerializer, DocumentSerializer, FolderDetailSerializer, FolderOpenSerializer



class RootFolderAndDocumentsAPIView(APIView):
    def get(self, request, IDcommunity):
        # Obtener todas las carpetas con el conteo de documentos
        folders = Folder.objects.filter(community=IDcommunity, parent_folder_id=0)
        folder_data = []

        for folder in folders:
            document_count = Document.objects.filter(community=IDcommunity, folder_id=folder.folder_id).count()
            folder_info = {
                'folder_id': folder.folder_id,
                'name': folder.name,
                'document_count': document_count
            }
            folder_data.append(folder_info)

        # Obtener documentos en el root (sin carpeta asignada)
        documents = Document.objects.filter(community=IDcommunity, folder_id=0)
        document_serializer = DocumentSerializer(documents, many=True)

        response_data = {
            'folders': folder_data,
            'documents': document_serializer.data
        }

        return Response(response_data)

class FolderListAPIView(APIView):
    def get(self, request, IDcommunity):
        folders = Folder.objects.filter(community=IDcommunity)
        folder_data = []

        for folder in folders:
            document_count = Document.objects.filter(community=IDcommunity, folder_id=folder.folder_id).count()
            folder_info = {
                'folder_id': folder.folder_id,
                'name': folder.name,
                'document_count': document_count
            }
            folder_data.append(folder_info)

        return Response(folder_data)
    
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
        folder = get_object_or_404(Folder, folder_id=IDfolder, community_id=IDcommunity)
        serializer = FolderSerializer(folder)
        return Response(serializer.data)

    def put(self, request, IDcommunity, IDfolder):
        folder = get_object_or_404(Folder, folder_id=IDfolder, community_id=IDcommunity)
        serializer = FolderSerializer(folder, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request, IDcommunity, IDfolder):
        folder = get_object_or_404(Folder, folder_id=IDfolder, community_id=IDcommunity)
        folder.delete()
        return Response(status=204)
    
class FolderOpenAPIView(APIView):
    def get(self, request, IDcommunity, IDfolder):
        folder = get_object_or_404(Folder, folder_id=IDfolder, community_id=IDcommunity)
        serializer = FolderDetailSerializer(folder)
        return Response(serializer.data)
    
class FolderOpenDetailView(APIView):
    def get(self, request, IDcommunity, IDfolder):
        folder = get_object_or_404(Folder, community_id=IDcommunity, folder_id=IDfolder)
        subfolders = Folder.objects.filter(community_id=IDcommunity, parent_folder_id=IDfolder)
        documents = Document.objects.filter(community_id=IDcommunity, folder_id=IDfolder)
        
        folder_data = FolderOpenSerializer(folder).data
        folder_data['subfolders'] = FolderListCompleteSerializer(subfolders, many=True).data
        folder_data['documents'] = DocumentSerializer(documents, many=True).data

        return Response(folder_data)

### Document views ###  
class DocumentUploadAPIView(APIView):
    def post(self, request, IDcommunity, IDfolder):
        data = request.data.copy()
        data['community'] = IDcommunity
        
        if IDfolder == '0':
            data['folder_id'] = None
        else:
            data['folder_id'] = IDfolder
            
        serializer = DocumentUploadSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
class DocumentDetailAPIView(APIView):
    def get(self, request, IDcommunity, IDdocument):
        document = get_object_or_404(Document, document_id=IDdocument, community_id=IDcommunity)
        serializer = DocumentSerializer(document)
        return Response(serializer.data)

class DocumentDeleteAPIView(APIView):
    def delete(self, request, IDcommunity, IDdocument):
        document = get_object_or_404(Document, document_id=IDdocument, community_id=IDcommunity)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DocumentDownloadAPIView(APIView):
    def get(self, request, IDcommunity, IDdocument):
        document = get_object_or_404(Document, document_id=IDdocument, community_id=IDcommunity)
        file_handle = document.file.open()
        response = FileResponse(file_handle, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{document.file.name}"'
        return response