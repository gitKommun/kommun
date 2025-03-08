from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Notification

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'surnames', 'language_config')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Community info'), {'fields': ('current_community',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'surnames', 'birthdate', 'address', 'phone_number', 'language_config', 'personal_id_number', 'personal_id_type', 'current_community'),
        }),
    )
    list_display = ('email', 'name', 'surnames', 'is_staff')
    search_fields = ('email', 'name', 'surnames')
    ordering = ('email',)

admin.site.register(User, UserAdmin)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipient', 'title', 'category', 'created_at', 'read')
    list_filter = ('read', 'category')
    search_fields = ('title', 'message', 'recipient__email')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Destinatario', {
            'fields': ('recipient',)
        }),
        ('Contenido', {
            'fields': ('title', 'message', 'link')
        }),
        ('Clasificación', {
            'fields': ('category',)
        }),
        ('Estado', {
            'fields': ('read', 'created_at')
        }),
    )
    
    readonly_fields = ('created_at',)
