from rest_framework import serializers
from .models import Document, Folder

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class FolderSerializer(serializers.ModelSerializer):
    folder_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Folder
        fields = '__all__'


class FolderListCompleteSerializer(serializers.ModelSerializer):
    document_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Folder
        fields = ['folder_id', 'name', 'document_count']



class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['name', 'file', 'community', 'folder_id']


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class FolderDetailSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Folder
        fields = ['id', 'name', 'community', 'documents']