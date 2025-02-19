from django.contrib import admin
from .models import CommonArea

class CommonAreaAdmin(admin.ModelAdmin):
    list_display = ('area_id', 'name', 'community', 'reservable', 'reservation_duration', 'time_unit')
    list_filter = ('community', 'reservable', 'time_unit')
    search_fields = ('name', 'community__nameCommunity')
    ordering = ('community', 'area_id')

    # Deshabilitar la edición de `area_id` en el admin
    readonly_fields = ('area_id',)

    def save_model(self, request, obj, form, change):
        """
        Si es un nuevo objeto, asigna automáticamente el `area_id` relativo a la comunidad.
        """
        if not obj.area_id:
            last_area = CommonArea.objects.filter(community=obj.community).order_by('area_id').last()
            obj.area_id = last_area.area_id + 1 if last_area else 1
        super().save_model(request, obj, form, change)

# Registrar el modelo en el panel de administración
admin.site.register(CommonArea, CommonAreaAdmin)
