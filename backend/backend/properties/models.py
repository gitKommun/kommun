from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
class Property(models.Model):
    PROPERTY_USAGE_CHOICES = (
        ('COMMERCIAL', 'Comercial'),
        ('STORAGE', 'Almacén-Estacionamiento'),
        ('RESIDENTIAL', 'Residencial'),
        ('INDUSTRIAL', 'Industrial'),
    )

    #Clave primaria
    community = models.ForeignKey('communities.Community', on_delete=models.CASCADE, related_name='properties')
    property_id = models.PositiveIntegerField()  # Número secuencial dentro de la comunidad

    #Datos economicos
    surface_area = models.DecimalField(_('surface area'), max_digits=10, decimal_places=2, null=True, blank=True)  # SUPERFICIE
    participation_coefficient = models.DecimalField(_('participation coefficient'), max_digits=5, decimal_places=4, null=True, blank=True)  # COEFICIENTE DE PARTICIPACIÓN
    usage = models.CharField(max_length=50, choices=PROPERTY_USAGE_CHOICES)

    #Ubicación
    address_complete = models.CharField(_('address'), max_length=200, null=True, blank=True)
    block = models.CharField(_('block'), max_length=50, null=True, blank=True)
    staircase = models.CharField(_('staircase'), max_length=50, null=True, blank=True)
    floor = models.CharField(_('floor'), max_length=50, null=True, blank=True)
    door = models.CharField(_('door'), max_length=50, null=True, blank=True)

    class Meta:
        # Clave primaria compuesta
        unique_together = (('community', 'property_id'),)
        ordering = ['community', 'property_id']
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")

    def __str__(self):
        return f"Property {self.property_id} in {self.community.name}"
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Si la propiedad no tiene una PK (es nueva)
            # Calcular el siguiente property_id para la comunidad
            last_property = Property.objects.filter(community=self.community).order_by('property_id').last()
            if last_property:
                self.property_id = last_property.property_id + 1
            else:
                self.property_id = 1
        super().save(*args, **kwargs)


class PropertyRelationship(models.Model):
    class RelationType(models.TextChoices):
        OWNER = 'owner', _('Owner')
        TENANT = 'tenant', _('Tenant')

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='relationships')
    type = models.CharField(max_length=10, choices=RelationType.choices, default=RelationType.OWNER)
    person = models.ForeignKey('communities.UserCommunityRole', on_delete=models.CASCADE, related_name='property_relationships')

    def __str__(self):
        return f"{self.user.name} - {self.role} of {self.property.number}"
    