from django.contrib import admin
from .models import Folder, Document

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('folder_id', 'name', 'community', 'parent_folder_id')
    list_filter = ('community',)
    search_fields = ('name', 'community__name')
    ordering = ('community', 'folder_id')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('document_id', 'name', 'community', 'folder_id', 'upload_user', 'upload_date', 'file')
    list_filter = ('community', 'upload_date')
    search_fields = ('name', 'community__name', 'upload_user__email')
    ordering = ('community', 'document_id')
    readonly_fields = ('document_id', 'upload_date')

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Si estamos editando un documento existente
            return self.readonly_fields + ('file',)
        return self.readonly_fields
