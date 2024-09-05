from django.contrib import admin
from .models import Community, UserCommunityRole
from django.utils.translation import gettext_lazy as _

class CommunityAdmin(admin.ModelAdmin):
    # Campos que se mostrarán en la lista de comunidades
    list_display = ('community_id', 'name', 'province', 'city', 'postal_code', 'cif', 'main_contact_user', 'configuration_is_completed')
    # Campos por los que se puede filtrar en la lista
    list_filter = ('province', 'configuration_is_completed')
    # Campos por los que se puede buscar
    search_fields = ('name', 'cif', 'address', 'province')
    # Campos editables directamente desde la lista de comunidades
    list_editable = ('configuration_is_completed',)
    # Campos de solo lectura
    readonly_fields = ('community_id',)

    # Secciones para organizar los campos en el formulario de detalle
    fieldsets = (
        (None, {
            'fields': ('community_id', 'name', 'main_contact_user', 'configuration_is_completed', 'image'),
        }),
        (_('Location Info'), {
            'fields': ('address', 'city', 'province', 'postal_code'),
        }),
        (_('Legal Info'), {
            'fields': ('cif', 'catastral_ref'),
        }),
    )

    # Define el orden de las comunidades en la lista (opcional)
    ordering = ('name',)

admin.site.register(Community, CommunityAdmin)

class UserCommunityRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'community')

    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'community__name')

admin.site.register(UserCommunityRole, UserCommunityRoleAdmin)