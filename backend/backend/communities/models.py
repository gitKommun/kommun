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
        return f"{self.community_id} - {self.address}, {self.city} "
    
class PersonCommunity(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='people')
    person_id = models.PositiveIntegerField() # Número secuencial dentro de la comunidad

    #Personal data
    email = models.EmailField(_('email address'))
    name = models.CharField(_('name'), max_length=30)
    surnames = models.CharField(_('surnames'), max_length=120)
    birthdate = models.DateField(verbose_name=_("Birthdate"), null=True, blank=True)
    address = models.CharField(_('postal address'), null=True, blank=True, max_length=255)
    phone_number = models.CharField(_('phone number'), max_length=20, null=True, blank=True)
    personal_id_number = models.CharField(_('user ID'), max_length=20, null=True, blank=True)  # DNI, NIE, or passport
    personal_id_type = models.CharField(_('document type'), null=True, blank=True, max_length=20, choices=[('DNI', 'DNI'), ('NIE', 'NIE'), ('PASSPORT', 'Passport')])

    class Meta:
        # Clave primaria compuesta
        unique_together = (('community', 'person_id'), ('community', 'email'))
        ordering = ['community']

    def __str__(self):
        return f"{self.name} {self.surnames}"
    
    def save(self, *args, **kwargs):
        if not self.person_id:  # Asegúrate de que solo asignamos person_id si aún no ha sido asignado
            last_person = PersonCommunity.objects.filter(community=self.community).order_by('person_id').last()
            if last_person:
                self.person_id = last_person.person_id + 1
            else:
                self.person_id = 1

        super().save(*args, **kwargs)

class Role(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class UserCommunityRole(models.Model):
    USER_STATUS = (
        ('active', 'Activo'),
        ('disabled', 'Deshabilitado'),
        ('temp', 'Temporal'),
        ('not_registered', 'No registrado'),
    )
    
    #Clave primaria
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='user_roles')
    neighbour_id = models.PositiveIntegerField()  # Número secuencial dentro de la comunidad

    user = models.ForeignKey('members.User', on_delete=models.SET_NULL, related_name='roles', null=True, blank=True)
    person = models.ForeignKey(PersonCommunity, on_delete=models.SET_NULL, related_name='roles', null=True, blank=True)
    
    roles = models.ManyToManyField(Role)  # Relación muchos a muchos con la tabla de roles
    user_status = models.CharField(max_length=14, choices=USER_STATUS, default='active')

    class Meta:
        unique_together = (('community', 'neighbour_id'), ('user', 'community'), ('person', 'community'))


    def clean(self):
        # Asegurarse de que al menos uno de los campos esté presente
        if not self.user and not self.person:
            raise ValidationError('Debe haber al menos un user o un person asignado.')
        
        # Verificar que ambos campos no estén vacíos
        if self.user and self.person:
            raise ValidationError('No puede haber un user y un person al mismo tiempo. Solo uno debe ser asignado.')

    def save(self, *args, **kwargs):
        # Llamar a la validación manualmente
        self.clean()
        super().save(*args, **kwargs)


