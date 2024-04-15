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
    address = models.CharField(_('address'), max_length=255) #calle, y si tiene numero 
    city = models.CharField(_('city'), max_length=100)
    postal_code = models.CharField(_('postal code'), max_length=12)

    #contacto principal de la comunidad
    main_contact_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    main_contact_id = models.PositiveIntegerField(null=True, blank=True)
    mainContact = GenericForeignKey('main_contact_type', 'main_contact_id')

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
    IDproperty = models.CharField(
        _('property ID'), max_length=40, unique=True, primary_key=True
    ) #CIF Community + property_number
    community = models.ForeignKey(Community, on_delete=models.CASCADE, verbose_name=_('community'))
    numberProperty = models.CharField(_('property number'), max_length=50)
    owner = models.ForeignKey('members.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('owner'))
    typeProperty = models.CharField(_('property type'), max_length=50, choices=[('HOUSE', _('House')), ('PARKING', _('Parking')), ('OTHER', _('Other'))])
    communityPropertyPercentage = models.FloatField(verbose_name=_('community property percentage'), null=True, blank=True)

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")

    def __str__(self):
        return f"{self.numberProperty} - {self.community.address} ({self.typeProperty})"
    
    def save(self, *args, **kwargs):
        if not self.IDproperty:
            self.IDproperty = f"{self.community_id}{self.numberProperty}"
        super(Property, self).save(*args, **kwargs)

    
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
