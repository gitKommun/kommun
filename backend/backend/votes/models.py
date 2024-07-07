from django.db import models
from django.utils.translation import gettext_lazy as _
from members.models import User
from communities.models import Community

class Vote(models.Model):
    class VoteType(models.TextChoices):
        SIMPLE = 'simple', _('Simple (Yes/No)')
        MULTIPLE_CHOICE = 'multiple_choice', _('Multiple Choice')
        RANKING = 'ranking', _('Ranking')

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)
    start_date = models.DateTimeField(_('start date'))
    end_date = models.DateTimeField(_('end date'))
    vote_type = models.CharField(_('vote type'), max_length=20, choices=VoteType.choices)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_votes')
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='votes')
    eligible_voters = models.ManyToManyField(User, related_name='eligible_votes')

    def __str__(self):
        return f"{self.title} ({self.community.nameCommunity})"

class Option(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(_('text'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)

    def __str__(self):
        return self.text

class VoteRecord(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, related_name='vote_records')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vote_records')
    option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, blank=True, related_name='vote_records')
    options = models.ManyToManyField(Option, related_name='vote_records_multiple', blank=True)
    timestamp = models.DateTimeField(_('timestamp'), auto_now_add=True)
    recorded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recorded_votes')

    class Meta:
        unique_together = ('vote', 'user')

    def __str__(self):
        return f"VoteRecord for {self.user.email} on {self.vote.title}"
