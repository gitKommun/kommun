import os

from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser


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
            'subfolders': folder_data,
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
        folders = Folder.objects.filter(community_id=IDcommunity, parent_folder_id=IDfolder)
        documents = Document.objects.filter(community_id=IDcommunity, folder_id=IDfolder)
        
        # Construir el path
        path = []
        current_folder = folder
        while current_folder.parent_folder_id is not None:
            parent_folder = Folder.objects.filter(community=current_folder.community, folder_id=current_folder.parent_folder_id).first()
            if not parent_folder:
                break
            path.append({
                'folder_id': parent_folder.folder_id,
                'name': parent_folder.name
            })
            current_folder = parent_folder
        path.reverse()  # Path en orden desde el root hasta la carpeta actual

        # Añadir el folder actual al path
        path.append({
            'folder_id': folder.folder_id,
            'name': folder.name
        })

        documents_data = DocumentSerializer(documents, many=True).data

        result = {
            'folders': FolderListCompleteSerializer(folders, many=True).data,
            'documents': documents_data,
            'path': path
        }

        return Response(result)

class OLDFolderOpenDetailView(APIView):
    def get(self, request, IDcommunity, IDfolder):
        folder = get_object_or_404(Folder, community_id=IDcommunity, folder_id=IDfolder)
        subfolders = Folder.objects.filter(community_id=IDcommunity, parent_folder_id=IDfolder)
        documents = Document.objects.filter(community_id=IDcommunity, folder_id=IDfolder)
        
        folder_data = {}
        documents_data = {}
        folder_data['folders'] = FolderOpenSerializer(folder).data.folder_id
        folder_data['subfolders'] = FolderListCompleteSerializer(subfolders, many=True).data
        documents_data['documents'] = DocumentSerializer(documents, many=True).data

        result = {
            'folders': [folder_data],
            'documents': [documents_data],
            'path': ""
        }

        return Response(result)

### Document views ###  


class DocumentMultiUploadAPIView(APIView):
    parser_classes = [MultiPartParser]
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
    MAX_TOTAL_SIZE = 50 * 1024 * 1024  # 50 MB
    MAX_FILES = 10  # Maximum number of files per upload

    def post(self, request, IDcommunity, IDfolder):
        documents_data = request.FILES.getlist('file')
        #print(request.FILES)
        #print(documents_data)

        # Check number of files
        if len(documents_data) > self.MAX_FILES:
            return Response({'error': f'Cannot upload more than {self.MAX_FILES} files at a time.'}, status=status.HTTP_400_BAD_REQUEST)
        
        total_size = sum([doc.size for doc in documents_data])

        # Check total size
        if total_size > self.MAX_TOTAL_SIZE:
            return Response({'error': f'Total upload size cannot exceed {self.MAX_TOTAL_SIZE / (1024 * 1024)} MB.'}, status=status.HTTP_400_BAD_REQUEST)
        
        response_data = []

        for document_data in documents_data:
            print(document_data.name)
            # Check individual file size
            if document_data.size > self.MAX_FILE_SIZE:
                return Response({'error': f'File "{document_data.name}" exceeds the maximum file size of {self.MAX_FILE_SIZE / (1024 * 1024)} MB.'}, status=status.HTTP_400_BAD_REQUEST)
            
            data = {
                'name': document_data.name,
                'file': document_data,
                'community': IDcommunity,
                'folder_id': IDfolder if IDfolder != '0' else None,
            }
            
            serializer = DocumentUploadSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(response_data, status=status.HTTP_201_CREATED)
    
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
        filename = os.path.basename(document.file.name)
        response = FileResponse(file_handle, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response