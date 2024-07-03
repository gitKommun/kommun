from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
from communities.models import Community
from members.models import User

class CommonArea(models.Model):
    TIME_UNIT_CHOICES = [
        ('MIN', 'Minutes'),
        ('HOUR', 'Hours'),
        ('DAY', 'Days'),
    ]

    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='common_areas')
    area_id = models.PositiveIntegerField(null=True, blank=True)  # Número secuencial dentro de la comunidad
    name = models.CharField(_('name'), max_length=100)
    type = models.CharField(_('type'), max_length=50, null=True, blank=True)
    reservable = models.BooleanField(_('reservable'), default=False)
    reservation_duration = models.PositiveIntegerField(_('reservation duration'), null=True, blank=True)
    time_unit = models.CharField(_('time unit'), max_length=4, choices=TIME_UNIT_CHOICES, null=True, blank=True)

    class Meta:
        #unique_together = (('community', 'area_id'),)
        #ordering = ['community', 'area_id']
        verbose_name = _("Common Area")
        verbose_name_plural = _("Common Areas")

    def save(self, *args, **kwargs):
        if not self.pk:
            # Calcular el siguiente area_id para la comunidad
            last_area = CommonArea.objects.filter(community=self.community).order_by('area_id').last()
            if last_area:
                self.area_id = last_area.area_id + 1
            else:
                self.area_id = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Common Area {self.area_id} - {self.name} ({self.community.nameCommunity})"
    


class Reservation(models.Model):
    TIME_UNIT_CHOICES = [
        ('MIN', 'Minutes'),
        ('HOUR', 'Hours'),
        ('DAY', 'Days'),
    ]

    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='reservations')
    common_area = models.ForeignKey(CommonArea, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    start_time = models.DateTimeField(_('start time'))
    end_time = models.DateTimeField(_('end time'))
    duration = models.PositiveIntegerField(_('duration'))
    time_unit = models.CharField(_('time unit'), max_length=4, choices=TIME_UNIT_CHOICES)

    class Meta:
        ordering = ['start_time']
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")
        unique_together = ('common_area', 'start_time', 'end_time')

    def __str__(self):
        return f"Reservation for {self.common_area.name} by {self.user.email} from {self.start_time} to {self.end_time}"