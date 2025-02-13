import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from members.models import User
from communities.models import Community, PersonCommunity

class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vote_id = models.PositiveIntegerField() 
    
    class VoteType(models.TextChoices):
        SIMPLE = 'simple', _('Simple (Yes/No)')
        MULTIPLE_CHOICE = 'multiple_choice', _('Multiple Choice')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)
    start_date = models.DateTimeField(_('start date'))
    end_date = models.DateTimeField(_('end date'))
    vote_type = models.CharField(_('vote type'), max_length=20, choices=VoteType.choices)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_votes')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='votes')
    eligible_voters = models.ManyToManyField(PersonCommunity, related_name='eligible_votes')

    class Meta:
        unique_together = ('community', 'vote_id')  # Asegura que vote_id sea único dentro de la comunidad
        ordering = ['vote_id']  # Ordena por vote_id dentro de la comunidad

    def __str__(self):
        return f"{self.title} ({self.community.name})"

    def save(self, *args, **kwargs):
        if not self.vote_id:  # Si no se ha asignado un vote_id
            last_vote = Vote.objects.filter(community=self.community).order_by('vote_id').last()
            if last_vote:
                self.vote_id = last_vote.vote_id + 1
            else:
                self.vote_id = 1  # Primer voto de la comunidad
        super().save(*args, **kwargs)

class Option(models.Model):
    option_id = models.PositiveIntegerField()
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(_('option_text'), max_length=255)

    def __str__(self):
        return self.option_text
    
    def save(self, *args, **kwargs):
        if not self.option_id:  # Si no se ha asignado un vote_id
            last_option = Option.objects.filter(vote=self.vote).order_by('option_id').last()
            if last_option:
                self.option_id = last_option.option_id + 1
            else:
                self.option_id = 1  # Primer voto de la comunidad
        super().save(*args, **kwargs)

class VoteRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='vote_records')
    neighbor = models.ForeignKey(PersonCommunity, on_delete=models.CASCADE, related_name='vote_records') #Owner of the vote
    options = models.ManyToManyField(Option, related_name='vote_records_multiple', blank=True)

    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recorded_votes')

    delegated_to = models.ForeignKey(PersonCommunity, on_delete=models.CASCADE, null=True, blank=True, related_name='delegated_votes')    
    class Meta:
        unique_together = ('vote', 'neighbor')

    def __str__(self):
        return f"VoteRecord for {self.neighbor.name} {self.neighbor.surnames} on {self.vote.title}"