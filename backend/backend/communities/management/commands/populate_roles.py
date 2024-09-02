from django.core.management.base import BaseCommand
from communities.models import Role

class Command(BaseCommand):
    help = 'Populate the database with default roles'

    def handle(self, *args, **kwargs):
        roles = ['owner', 'tenant', 'admin']

        for role_name in roles:
            role, created = Role.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Role "{role_name}" created'))
            else:
                self.stdout.write(f'Role "{role_name}" already exists')
