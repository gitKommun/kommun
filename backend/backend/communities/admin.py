from django.contrib import admin
from .models import Community

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('IDcommunity', 'nameCommunity', 'address', 'city', 'postal_code')
    search_fields = ('nameCommunity', 'address', 'city')
    list_filter = ('city',)

# Puedes hacer lo mismo con otros modelos:
from .models import Property, PersonCommunity

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('community', 'numberProperty', 'typeProperty', 'communityPropertyPercentage')
    search_fields = ('numberProperty', 'typeProperty')

@admin.register(PersonCommunity)
class PersonCommunityAdmin(admin.ModelAdmin):
    list_display = ('community', 'name', 'surnames', 'email', 'phone_number')
    search_fields = ('name', 'surnames', 'email')
