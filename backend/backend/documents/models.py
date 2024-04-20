from datetime import timezone
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
# Create your models here.

class Folder(models.Model):
    name = models.CharField(max_length=255)
    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, null=True, blank=True)
    #userCreator = models.ForeignKey('members.User', on_delete=models.CASCADE, null=True, blank=True)
    #created_at = models.DateTimeField(auto_now_add=True)


valid_formats = [
        'application/pdf',
        'text/plain',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'image/jpeg',
        'image/png',
    ]

def document_path(community, filename):
    return f'documents/{community.pk}/{filename}'

class Document(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=document_path, validators=[FileExtensionValidator(allowed_extensions=valid_formats)], storage=settings.DOCUMENT_STORAGE)
    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE)
    #userCreator = models.ForeignKey('members.User', on_delete=models.SET_NULL, null=True, blank=True) #TO DO añadir logica para mantener el nombre del usuario creador en caso de eliminar el usuario
    #created_at = models.DateTimeField(auto_now_add=True)
    #log = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.log = []
        super().save(*args, **kwargs)

    def add_log_change(self, user, change_type):
        self.log.append({
            'user': user.username,
            'date': timezone.now(),
            'type': change_type,
        })
        self.save(update_fields=['log'])



    
    