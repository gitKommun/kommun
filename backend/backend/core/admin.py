from django.contrib import admin
from .models import Province, Municipality, PostalCode

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']  # Muestra el nombre y código de la provincia en la lista del admin
    search_fields = ['name', 'code']  # Permite buscar por nombre y código

class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')
    search_fields = ('name', 'code_ine')
    list_filter = ('province__name', 'province__code')  # Filtrado por código y nombre de la provincia

admin.site.register(Municipality, MunicipalityAdmin)

class PostalCodeAdmin(admin.ModelAdmin):
    list_display = ('postal_code', 'municipality')  # Muestra el código postal y el municipio en la lista
    search_fields = ('postal_code', 'municipality__name')  # Habilita la búsqueda por código postal y nombre del municipio
    list_filter = ('municipality__province', 'municipality')  # Filtros para provincias y municipios

admin.site.register(PostalCode, PostalCodeAdmin)
