from django.contrib import admin


from django.utils.translation import gettext_lazy as _
from .models import Property, PropertyRelationship

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('community', 'property_id', 'surface_area', 'participation_coefficient', 'usage', 'address_complete', 'block', 'staircase', 'floor', 'door')
    list_filter = ('community', 'usage')
    search_fields = ('community', 'address_complete')
    ordering = ('community', 'property_id')
    fieldsets = (
        (None, {
            'fields': ('community', 'property_id', 'surface_area', 'participation_coefficient', 'usage'),
        }),
        (_('Location Info'), {
            'fields': ('address_complete', 'block', 'staircase', 'floor', 'door'),
        }),
    )

admin.site.register(Property, PropertyAdmin)


class PropertyRelationshipAdmin(admin.ModelAdmin):
    list_display = ('property', 'type', 'person')
    list_filter = ('property', 'type')
    search_fields = ('property', 'person')
    ordering = ('property', 'type')
    fieldsets = (
        (None, {
            'fields': ('property', 'type', 'person'),
        }),
    )

admin.site.register(PropertyRelationship, PropertyRelationshipAdmin)
