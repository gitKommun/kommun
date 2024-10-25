from django.contrib import admin
from .models import Vote, Option, VoteRecord



class VoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'community', 'start_date', 'end_date', 'vote_type', 'created_by')
    list_filter = ('community', 'vote_type', 'start_date', 'end_date')
    search_fields = ('title', 'community__name', 'created_by__email')
    
    ordering = ('community', 'vote_id')

    def save_model(self, request, obj, form, change):
        """
        Override to handle auto-incrementing `vote_id` when creating a new vote.
        """
        if not obj.vote_id:
            # Calcular el próximo vote_id para la comunidad
            last_vote = Vote.objects.filter(community=obj.community).order_by('vote_id').last()
            if last_vote:
                obj.vote_id = last_vote.vote_id + 1
            else:
                obj.vote_id = 1
        super().save_model(request, obj, form, change)

class VoteRecordAdmin(admin.ModelAdmin):
    list_display = ('vote', 'neighbor', 'delegated_to', 'timestamp', 'recorded_by')
    list_filter = ('vote', 'neighbor', 'delegated_to', 'timestamp')
    search_fields = ('vote__title', 'neighbor__name', 'neighbor__surnames', 'delegated_to__name', 'recorded_by__email')

admin.site.register(Vote, VoteAdmin)
admin.site.register(VoteRecord, VoteRecordAdmin)
