import uuid

from django.db import models
from datetime import timezone

from communities.models import Community

class Plan(models.Model):
    """Define los planes de suscripción disponibles."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)  # Ejemplo: "Básico", "Premium", "Enterprise"
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    accessible_endpoints = models.JSONField(default=dict)  # Controla los módulos/endpoints accesibles

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """Gestión de suscripciones de comunidades a planes."""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('expired', 'Expired')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    stripe_subscription_id = models.CharField(max_length=100, blank=True, null=True)  # ID de Stripe

    def __str__(self):
        return f"{self.community.name} - {self.plan.name} ({self.status})"

    def is_active(self):
        return self.status == 'active' and self.end_date >= timezone.now()
