from django.contrib import admin
from .models import Vote, Option, VoteRecord

class OptionInline(admin.TabularInline):
    model = Option
    extra = 1

class VoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'community', 'start_date', 'end_date', 'vote_type', 'created_by')
    list_filter = ('community', 'vote_type', 'start_date', 'end_date')
    search_fields = ('title', 'community__name', 'created_by__email')
    inlines = [OptionInline]  # Mostrar las opciones en línea dentro del voto
    ordering = ('community', 'vote_id')

class VoteRecordAdmin(admin.ModelAdmin):
    list_display = ('vote', 'neighbor', 'delegated_to', 'timestamp', 'recorded_by')
    list_filter = ('vote', 'neighbor', 'delegated_to', 'timestamp')
    search_fields = ('vote__title', 'neighbor__name', 'neighbor__surnames', 'delegated_to__name', 'recorded_by__email')

admin.site.register(Vote, VoteAdmin)
admin.site.register(VoteRecord, VoteRecordAdmin)
