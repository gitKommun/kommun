from rest_framework.permissions import BasePermission
from subscriptions.models import Subscription
from django.utils import timezone

class HasSubscriptionPermission(BasePermission):
    """
    Permiso para verificar si una comunidad tiene acceso a un módulo en función de su plan.
    """

    def has_permission(self, request, view):
        community_id = request.parser_context['kwargs'].get('IDcommunity')
        if not community_id:
            return False

        subscription = Subscription.objects.filter(
            community__community_id=community_id,
            status='active',
            end_date__gte=timezone.now()
        ).first()

        if not subscription:
            return False

        allowed_modules = subscription.plan.accessible_endpoints.get('modules', [])
        request_path = request.path.lower()

        # Verificar si el endpoint solicitado está dentro de los accesibles
        return any(module in request_path for module in allowed_modules)
