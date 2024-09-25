import uuid
from django.utils import timezone 
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

def generate_idcommunity_default():
    return str(uuid.uuid4()).replace('-', '')[:12]

def document_path(instance, filename):
    # Extrae la extensión del archivo
    extension = filename.split('.')[-1]
    # Genera un nombre único para el archivo
    new_filename = f'community_image.{extension}'
    # Retorna la ruta completa incluyendo el nuevo nombre del archivo
    return f'documents/{instance.community_id}/{new_filename}'

class Community(models.Model):
    community_id = models.CharField(
        max_length=12, 
        unique=True, 
        default=generate_idcommunity_default,  
        primary_key=True
    )
    
    name = models.CharField(_('community name'), max_length=40, default='Mi comunidad') #Nombre residencial
    address = models.CharField(_('address'), max_length=255, null=True, blank=True) #Calle, y si tiene numero 
    city = models.ForeignKey('core.Municipality', on_delete=models.SET_NULL, related_name='communities', null=True, blank=True)
    province = models.ForeignKey('core.Province', on_delete=models.SET_NULL, related_name='communities', null=True, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=12, null=True, blank=True)

    cif = models.CharField(_('community nif'), max_length=20, unique=True, null=True, blank=True) #CIF Community / Opcional
    catastral_ref = models.CharField(_('catastral reference'), max_length=50, null=True, blank=True) #Referencia Catastral

    main_contact_user = models.ForeignKey('members.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='communities_main') #Contacto principal de la comunidad
    configuration_is_completed = models.BooleanField(null=True, blank=True)

    image = models.ImageField(null=True, blank=True, upload_to=document_path) # TODO: Pendiente configurar

    class Meta:
        verbose_name = _("Community")
        verbose_name_plural = _("Communities")

    def __str__(self):
        return f"{self.name} - {self.city}, {self.province} "

class Role(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class PersonCommunity(models.Model):
    USER_STATUS = (
        ('active', 'Activo'),
        ('disabled', 'Deshabilitado'),
        ('temp', 'Temporal'),
        ('not_registered', 'No registrado'),
    )

    #PK
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='people')
    person_id = models.PositiveIntegerField() # Número secuencial dentro de la comunidad

    user = models.ForeignKey('members.User', on_delete=models.SET_NULL, related_name='profiles', null=True, blank=True)

    roles = models.ManyToManyField(Role, null=True, blank=True)  # Relación muchos a muchos con la tabla de roles
    user_status = models.CharField(max_length=14, choices=USER_STATUS, null=True, blank=True)

    #Profile data
    email = models.EmailField(_('email address'), null=True, blank=True)
    name = models.CharField(_('name'), null=True, blank=True, max_length=30)
    surnames = models.CharField(_('surnames'), null=True, blank=True, max_length=120)
    birthdate = models.DateField(verbose_name=_("Birthdate"), null=True, blank=True)
    address = models.CharField(_('postal address'), null=True, blank=True, max_length=255)
    phone_number = models.CharField(_('phone number'), max_length=20, null=True, blank=True)
    personal_id_number = models.CharField(_('user ID'), max_length=20, null=True, blank=True)  # DNI, NIE, or passport
    personal_id_type = models.CharField(_('document type'), null=True, blank=True, max_length=20, choices=[('DNI', 'DNI'), ('NIE', 'NIE'), ('PASSPORT', 'Passport')])

    class Meta:
        # Clave primaria compuesta
        unique_together = (('community', 'person_id'))
        ordering = ['community']

    def __str__(self):
        return f"{self.name} {self.surnames}"
    
    def save(self, *args, **kwargs):
        if not self.person_id:  
            last_person = PersonCommunity.objects.filter(community=self.community).order_by('person_id').last()
            if last_person:
                self.person_id = last_person.person_id + 1
            else:
                self.person_id = 1

        super().save(*args, **kwargs)

