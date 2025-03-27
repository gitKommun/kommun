from django.db import models
from django.contrib.auth import get_user_model
from communities.models import Community
import uuid

User = get_user_model()

class Claim(models.Model):
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('in_process', 'In Process'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    CATEGORY_CHOICES = [
        ('maintenance', 'Maintenance'),
        ('cleaning', 'Cleaning'),
        ('security', 'Security'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='claims')
    claim_id = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims') 
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='information')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    incident_date = models.DateTimeField(null=True, blank=True)
    problem_persists = models.BooleanField(default=True)
    #image = models.ImageField(upload_to='claims_images/', null=True, blank=True)
    #assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_claims')
    #assignet_toName = models.CharField(max_length=255, null=True, blank=True) 

    current_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    last_status_change = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.status}"

    def save(self, *args, **kwargs):
        if not self.claim_id:  # Si no se ha asignado un claim_id
            last_vote = Claim.objects.filter(community=self.community).order_by('claim_id').last()
            if last_vote:
                self.claim_id = last_vote.claim_id + 1
            else:
                self.claim_id = 1  # Primer voto de la comunidad
        super().save(*args, **kwargs)


class ClaimStatusRecord(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='status_records')
    status = models.CharField(max_length=20, choices=Claim.STATUS_CHOICES)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='status_changes')
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.claim.title} - {self.status} at {self.timestamp}"
    
    @property
    def changed_by_full_name(self):
        return f"{self.changed_by.name} {self.changed_by.surnames}"


class ClaimComment(models.Model):
    claim_comment_id = models.PositiveIntegerField()
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claim_comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.claim}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Solo se asigna un id relativo al crear un nuevo comentario
            last_comment = ClaimComment.objects.filter(claim=self.claim).order_by('claim_comment_id').last()
            self.claim_comment_id = (last_comment.claim_comment_id + 1) if last_comment else 1
        super().save(*args, **kwargs)


class ClaimMessage(models.Model):
    MESSAGE_TYPES = [
        ('info', 'Información'),
        ('update', 'Actualización'),
        ('important', 'Importante'),
        ('work_order', 'Orden de Trabajo'),
    ]

    message_id = models.PositiveIntegerField()  # ID relativo dentro de la incidencia
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='claim_messages')
    message = models.TextField()
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['claim', 'message_id']  # Asegurar que el ID es único dentro de la incidencia

    def __str__(self):
        return f"#{self.message_id} - {self.get_message_type_display()} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Solo se asigna un id relativo al crear un nuevo mensaje
            last_message = ClaimMessage.objects.filter(claim=self.claim).order_by('message_id').last()
            self.message_id = (last_message.message_id + 1) if last_message else 1
        super().save(*args, **kwargs)
   