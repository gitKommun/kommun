from rest_framework import serializers
from .models import Plan, Subscription

# 1️⃣ Serializer para los planes de suscripción
class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'description', 'price', 'accessible_endpoints']

# 2️⃣ Serializer para las suscripciones
class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)  # Incluye los detalles del plan

    class Meta:
        model = Subscription
        fields = ['id', 'community', 'plan', 'start_date', 'end_date', 'is_active']
        read_only_fields = ['id', 'start_date', 'end_date', 'is_active']
