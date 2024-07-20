from rest_framework import serializers
from .models import Document, Folder

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        #fields = '__all__'
        exclude = ['community']

class FolderSerializer(serializers.ModelSerializer):
    folder_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Folder
        fields = '__all__'


class FolderListCompleteSerializer(serializers.ModelSerializer):
    document_count = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ['folder_id', 'name', 'document_count']

    def get_document_count(self, obj):
        return Document.objects.filter(community=obj.community, folder_id=obj.folder_id).count()



class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['name', 'file', 'community', 'folder_id']




class FolderDetailSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Folder
        fields = ['id', 'name', 'community', 'documents']

class FolderOpenSerializer(serializers.ModelSerializer):
    document_count = serializers.IntegerField(read_only=True)
    path = serializers.SerializerMethodField()
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Folder
        fields = ['folder_id', 'name', 'document_count', 'path', 'documents']

    def get_path(self, obj):
        path = []
        current_folder = obj
        while current_folder.parent_folder_id != 0:
            parent_folder = Folder.objects.filter(community=current_folder.community, folder_id=current_folder.parent_folder_id).first()
            if parent_folder:
                path.insert(0, {"folder_id": parent_folder.folder_id, "name": parent_folder.name})
                current_folder = parent_folder
            else:
                break
        return path