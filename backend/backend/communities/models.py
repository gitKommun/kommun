from django.utils import timezone 
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import uuid

def generate_idcommunity_default():
    return str(uuid.uuid4()).replace('-', '')[:12]

class Community(models.Model):
    IDcommunity = models.CharField(
        max_length=12, 
        unique=True, 
        default=generate_idcommunity_default,  
        primary_key=True
    )
    NIFcommunity = models.CharField(_('community nif'), max_length=20, unique=True, null=True, blank=True) #CIF Community / Opcional
    nameCommunity = models.CharField(_('community name'), max_length=40, default='Mi comunidad') #nombre residencial
    address = models.CharField(_('address'), max_length=255, null=True, blank=True) #calle, y si tiene numero 
    city = models.CharField(_('city'), max_length=100, null=True, blank=True)
    postal_code = models.CharField(_('postal code'), max_length=12, null=True, blank=True)

    #contacto principal de la comunidad
    main_contact_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    main_contact_id = models.PositiveIntegerField(null=True, blank=True)
    mainContact = GenericForeignKey('main_contact_type', 'main_contact_id')

    #onboarding -> meter userDAta
    configurationCompleted = models.BooleanField(null=True, blank=True)
    numberProperties = models.IntegerField(_('number properties'), null=True, blank=True)
    numberHouses = models.IntegerField(_('number houses'), null=True, blank=True)

    class Meta:
        verbose_name = _("Community")
        verbose_name_plural = _("Communities")

    def __str__(self):
        return f"{self.IDcommunity} - {self.address}, {self.city} "

    def get_current_president(self):
        """Obtiene el presidente actual de la comunidad."""
        now = timezone.now()
        president = self.presidentcommunity_set.filter(startDate__lte=now, endDate__gte=now).first()
        return president.president if president else None

    def get_next_president(self):
        """Obtiene el próximo presidente de la comunidad."""
        now = timezone.now()
        president = self.presidentcommunity_set.filter(startDate__gt=now).order_by('startDate').first()
        return president.president if president else None

    
class Property(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='properties')
    property_id = models.PositiveIntegerField()  # Número secuencial dentro de la comunidad
    numberProperty = models.CharField(_('property number'), max_length=50)
    typeProperty = models.CharField(max_length=50, choices=[('HOUSE', 'House'), ('PARKING', 'Parking'), ('OTHER', 'Other')])
    communityPropertyPercentage = models.FloatField(null=True, blank=True)

    class Meta:
        # Clave primaria compuesta
        unique_together = (('community', 'property_id'),)
        ordering = ['community', 'property_id']
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")

    def __str__(self):
        return f"Property {self.property_id} in {self.community.name}"

class PersonCommunity(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='people')
    person_id = models.PositiveIntegerField() # Número secuencial dentro de la comunidad
    name = models.CharField(_('first name'), max_length=30)
    surnames = models.CharField(_('last name'), max_length=150)
    email = models.EmailField(_('email address'), null=True, blank=True) #TO DO: ver si se deja unique o se utiliza para linkar a usuarios existentes
    phone_number = models.CharField(_('phone number'), max_length=20, null=True, blank=True)
    user = models.ForeignKey('members.User', on_delete=models.CASCADE, null=True, blank=True, related_name='person_user')

    class Meta:
        # Clave primaria compuesta
        unique_together = (('community', 'person_id'),)
        ordering = ['community', 'person_id']

    def __str__(self):
        return f"{self.name} {self.surnames}"

class PresidentCommunity(models.Model):
    presidentCommunity = models.ForeignKey('members.User', on_delete=models.CASCADE, null=True, verbose_name=_('presidentCommunity'))
    presidencyCommunity = models.ForeignKey(Community, on_delete=models.CASCADE, verbose_name=_('community'), related_name='presidents')
    startDate = models.DateField(verbose_name=_("start date"), null=True, blank=True)
    endDate = models.DateField(verbose_name=_("end date"), null=True, blank=True)

    class Meta:
        verbose_name = _("President Community")
        verbose_name_plural = _("Presidents Community")


class AdministratorCommunity(models.Model):
    administratorCommunity = models.ForeignKey('members.User', on_delete=models.CASCADE, null=True, verbose_name=_('administratorCommunity'))
    administratedCommunity = models.ForeignKey(Community, on_delete=models.CASCADE, verbose_name=_('administratedCommunity'), related_name='administrators')
    startDate = models.DateField(verbose_name=_("start date"), null=True, blank=True)
    endDate = models.DateField(verbose_name=_("end date"), null=True, blank=True)
    
    class Meta:
        verbose_name = _("Administrator Community")
        verbose_name_plural = _("Administrators Communities")


class PropertyRelationship(models.Model):
    class Role(models.TextChoices):
        OWNER = 'owner', _('Owner')
        TENANT = 'tenant', _('Tenant')

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='relationships')
    #user = models.ForeignKey('members.User', on_delete=models.CASCADE, related_name='property_relationships')
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.OWNER)
    person = models.ForeignKey(PersonCommunity, on_delete=models.CASCADE, related_name='property_relationships')


    def __str__(self):
        return f"{self.user.name} - {self.role} of {self.property.number}"


class UserCommunityRole(models.Model):
    USER_ROLES = (
        ('owner', 'Propietario'),
        ('tenant', 'Inquilino'),
        ('admin', 'Administrador'),
    )

    USER_STATUS = (
        ('active', 'Activo'),
        ('disabled', 'Deshabilitado'),
        ('temp', 'Temporal'),
    )
    
    user = models.ForeignKey('members.User', on_delete=models.CASCADE, related_name='roles')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='user_roles')
    role = models.CharField(max_length=10, choices=USER_ROLES)
    user_status = models.CharField(max_length=10, choices=USER_STATUS, default='active')

    class Meta:
        unique_together = ('user', 'community', 'role', 'user_status')


