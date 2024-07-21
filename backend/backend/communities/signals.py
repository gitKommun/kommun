from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Community
from documents.models import Folder

@receiver(post_save, sender=Community)
def create_root_folder(sender, instance, created, **kwargs):
    if created:
        Folder.objects.create(
            name='root',
            community=instance,
            folder_id=0,
            parent_folder_id = None
        )
