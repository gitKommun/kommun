from django.contrib import admin
from .models import Claim, ClaimComment, ClaimStatusRecord

class ClaimAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('community', 'user', 'title', 'description', 'category', 'priority', 'status', 'incident_date', 'problem_persists')
        }),
    )
    ordering = ('-created_at',)

admin.site.register(Claim, ClaimAdmin)


# Register your models here.
