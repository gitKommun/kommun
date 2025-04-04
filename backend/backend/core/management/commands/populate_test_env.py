from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from communities.models import Community, PersonCommunity, Role
from properties.models import Property, PropertyRelationship
from claims.models import Claim
from votes.models import Vote, Option

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea un entorno de prueba con un usuario administrador y una comunidad'

    def handle(self, *args, **kwargs):
        try:
            # Crear usuario
            user, created = User.objects.get_or_create(
                email='admin@example.com',
                defaults={
                    'name': 'Juan',
                    'surnames': 'García López',
                }
            )
            
            if created:
                user.set_password('admin123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Usuario creado: {user.email}'))
            else:
                self.stdout.write(f'Usuario ya existe: {user.email}')

            # Crear comunidad
            community, created = Community.objects.get_or_create(
                name='Residencial Las Flores',
                defaults={
                    'address': 'Calle Principal 123',
                    'city': 'Madrid',
                    'postal_code': '28001',
                    'configuration_is_completed': True
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Comunidad creada: {community.name}'))
            else:
                self.stdout.write(f'Comunidad ya existe: {community.name}')

            # Obtener rol de administrador
            admin_role, _ = Role.objects.get_or_create(name='admin')

            # Crear perfil de persona en la comunidad
            person, created = PersonCommunity.objects.get_or_create(
                community=community,
                user=user,
                defaults={
                    'email': user.email,
                    'name': user.name,
                    'surnames': user.surnames,
                    'user_status': 'active'
                }
            )
            
            # Asignar rol de administrador
            if admin_role not in person.roles.all():
                person.roles.add(admin_role)
                self.stdout.write(self.style.SUCCESS(f'Rol de administrador asignado'))

            if created:
                self.stdout.write(self.style.SUCCESS(f'Perfil de persona creado y vinculado como admin'))
            else:
                self.stdout.write(f'Perfil de persona ya existe')

            # Crear 3 propietarios
            owners = []
            owner_data = [
                {'email': 'propietario1@example.com', 'name': 'María', 'surnames': 'López García'},
                {'email': 'propietario2@example.com', 'name': 'Carlos', 'surnames': 'Martínez Ruiz'},
                {'email': 'propietario3@example.com', 'name': 'Ana', 'surnames': 'Sánchez Pérez'},
            ]

            owner_role, _ = Role.objects.get_or_create(name='owner')

            for data in owner_data:
                user, created = User.objects.get_or_create(
                    email=data['email'],
                    defaults={
                        'name': data['name'],
                        'surnames': data['surnames'],
                    }
                )
                if created:
                    user.set_password('owner123')
                    user.save()

                person, _ = PersonCommunity.objects.get_or_create(
                    community=community,
                    user=user,
                    defaults={
                        'email': user.email,
                        'name': user.name,
                        'surnames': user.surnames,
                        'user_status': 'active'
                    }
                )
                person.roles.add(owner_role)
                owners.append(person)
                self.stdout.write(self.style.SUCCESS(f'Propietario creado: {user.email}'))

            # Crear 10 propiedades
            properties = []
            for i in range(1, 11):
                prop = Property.objects.create(
                    community=community,
                    surface_area=85.5,
                    participation_coefficient=0.0333,
                    usage='RESIDENCIAL',
                    block='A',
                    floor=str(i//2 + 1),
                    door=str(i%2 + 1)
                )
                properties.append(prop)
                self.stdout.write(self.style.SUCCESS(f'Propiedad creada: {prop}'))

            # Asignar 4 propiedades a propietarios
            for i in range(4):
                PropertyRelationship.objects.create(
                    community=community,
                    property=properties[i],
                    person=owners[i % 3],
                    type='owner'
                )
                self.stdout.write(self.style.SUCCESS(f'Propiedad {i+1} asignada a {owners[i % 3].name}'))

            # Crear 3 incidencias en diferentes estados
            claim_data = [
                {'title': 'Fuga de agua en portal', 'status': 'reported', 'priority': 'high'},
                {'title': 'Pintura deteriorada', 'status': 'in_process', 'priority': 'medium'},
                {'title': 'Luz fundida parking', 'status': 'resolved', 'priority': 'low'},
            ]

            for data in claim_data:
                claim = Claim.objects.create(
                    community=community,
                    created_by=owners[0].user,
                    title=data['title'],
                    description=f"Descripción de {data['title']}",
                    category='maintenance',
                    priority=data['priority'],
                    status=data['status'],
                    incident_date=timezone.now()
                )
                self.stdout.write(self.style.SUCCESS(f'Incidencia creada: {claim.title}'))

            # Crear 3 votaciones (2 abiertas, 1 cerrada)
            vote_data = [
                {
                    'title': 'Pintar fachada',
                    'start_date': timezone.now(),
                    'end_date': timezone.now() + timedelta(days=30),
                    'options': ['Azul', 'Beige', 'Blanco']
                },
                {
                    'title': 'Cambio empresa limpieza',
                    'start_date': timezone.now(),
                    'end_date': timezone.now() + timedelta(days=15),
                    'options': ['Empresa A', 'Empresa B']
                },
                {
                    'title': 'Instalación cámaras',
                    'start_date': timezone.now() - timedelta(days=30),
                    'end_date': timezone.now() - timedelta(days=1),
                    'options': ['Sí', 'No']
                }
            ]

            for data in vote_data:
                vote = Vote.objects.create(
                    community=community,
                    title=data['title'],
                    description=f"Votación sobre {data['title']}",
                    start_date=data['start_date'],
                    end_date=data['end_date'],
                    vote_type='multiple_choice',
                    created_by=user
                )
                
                # Crear opciones para cada votación
                for option_text in data['options']:
                    Option.objects.create(
                        vote=vote,
                        option_text=option_text
                    )
                
                # Añadir votantes elegibles
                vote.eligible_voters.add(*[owner for owner in owners])
                
                self.stdout.write(self.style.SUCCESS(f'Votación creada: {vote.title}'))

            # Obtener contadores
            property_count = Property.objects.filter(community=community).count()
            owner_count = PersonCommunity.objects.filter(community=community, roles__name='owner').count()
            admin_count = PersonCommunity.objects.filter(community=community, roles__name='admin').count()
            claim_count = Claim.objects.filter(community=community).count()
            vote_count = Vote.objects.filter(community=community).count()
            property_relationships = PropertyRelationship.objects.filter(community=community).count()

            self.stdout.write(self.style.SUCCESS(f"""
            Entorno de prueba configurado exitosamente:
            
            Usuario Administrador:
            - Email: {user.email}
            - Contraseña: admin123
            - Nombre: {user.name} {user.surnames}
            
            Comunidad:
            - ID: {community.community_id}
            - Nombre: {community.name}
            
            Perfil Admin:
            - ID: {person.person_id}
            - Estado: {person.user_status}

            Resumen de elementos creados:
            ═══════════════════════════
            ▸ {admin_count} Administrador(es)
            ▸ {owner_count} Propietarios
            ▸ {property_count} Propiedades
            ▸ {property_relationships} Propiedades asignadas
            ▸ {claim_count} Incidencias
            ▸ {vote_count} Votaciones

            Credenciales de acceso:
            ═══════════════════════════
            Admin:
            - Email: admin@example.com
            - Contraseña: admin123
            
            Propietarios:
            - Email: propietarioX@example.com (X = 1,2,3)
            - Contraseña: owner123
            """))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
