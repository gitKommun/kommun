from django.db import models
from django.contrib.auth import get_user_model
from communities.models import Community

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
        # Agregar más categorías según sea necesario
    ]
    
    PRIORITY_CHOICES = [
        ('information', 'Information'),
        ('complaint', 'Complaint'),
        ('important', 'Important'),
        ('urgent', 'Urgent'),
    ]

    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='claims')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims')
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='information')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    incident_date = models.DateTimeField(null=True, blank=True)
    problem_persists = models.BooleanField(default=True)
    #image = models.ImageField(upload_to='claims_images/', null=True, blank=True)
    #assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_claims')

    def __str__(self):
        return f"{self.title} - {self.status}"

class ClaimStatusRecord(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='status_records')
    status = models.CharField(max_length=20, choices=Claim.STATUS_CHOICES)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='status_changes')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.claim.title} - {self.status} at {self.timestamp}"

class ClaimComment(models.Model):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claim_comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.claim}"
