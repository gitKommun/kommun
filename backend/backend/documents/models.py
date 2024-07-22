from datetime import timezone
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

# Añadir parents - jerarquias

class Folder(models.Model):
    name = models.CharField(max_length=255)
    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, null=True, blank=True)
    #userCreator = models.ForeignKey('members.User', on_delete=models.CASCADE, null=True, blank=True)
    #created_at = models.DateTimeField(auto_now_add=True)
    folder_id = models.PositiveIntegerField()  # ID relativo autoincremental
    parent_folder_id = models.PositiveIntegerField(null=True, blank=True, default=0)  # ID del folder padre

    class Meta:
        unique_together = ('community', 'folder_id')
        ordering = ['community', 'folder_id']

    def save(self, *args, **kwargs):
        if self.folder_id is None:
                last_folder = Folder.objects.filter(community=self.community).order_by('folder_id').last()
                self.folder_id = last_folder.folder_id + 1 if last_folder else 1
        super().save(*args, **kwargs)

valid_formats = [
    'pdf',
    'txt',
    'doc',
    'docx',
    'jpeg',
    'jpg',
    'png',
    'xls',
    'xlsx',
    'csv'
]
def document_path(instance, name):
    #return f'documents/{community.pk}/{filename}'
    return f'documents/{instance.community.pk}/{name}'

class Document(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=document_path, validators=[FileExtensionValidator(allowed_extensions=valid_formats)])
    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE)
    folder_id = models.PositiveIntegerField(null=True, blank=True, default=0)  # ID relativo de la carpeta
    #folder = models.ForeignKey(Folder, related_name='documents', on_delete=models.CASCADE, null=True, blank=True)
    #userCreator = models.ForeignKey('members.User', on_delete=models.SET_NULL, null=True, blank=True) #TO DO añadir logica para mantener el nombre del usuario creador en caso de eliminar el usuario
    #created_at = models.DateTimeField(auto_now_add=True)
    #log = models.JSONField(null=True, blank=True)
    document_id = models.PositiveIntegerField()  # ID relativo autoincremental

    class Meta:
        unique_together = ('community', 'document_id')
        ordering = ['community', 'document_id']

    def save(self, *args, **kwargs):
        if not self.document_id:
            last_document = Document.objects.filter(community=self.community).order_by('document_id').last()
            self.document_id = last_document.document_id + 1 if last_document else 1

        if not self.pk:
            self.log = []
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def add_log_change(self, user, change_type):
        self.log.append({
            'user': user.username,
            'date': timezone.now(),
            'type': change_type,
        })
        self.save(update_fields=['log'])



    
    