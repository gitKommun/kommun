from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Community
from documents.models import Folder, Document

@receiver(post_save, sender=Community)
def create_root_folder(sender, instance, created, **kwargs):
    if created:
        Folder.objects.create(
            name='root',
            community=instance,
            folder_id=0,
            parent_folder_id = None
        )

         # Crear instancias de Document para las plantillas
        template_files = [
            'Guia_Gestion.pdf',
            ]

        for template_file in template_files:
            Document.objects.create(
                name=template_file,
                community=instance,
                folder_id=0,
                file=f'00.templates/{template_file}'  # Apunta al archivo de plantilla
            )
