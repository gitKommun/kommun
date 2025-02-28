from django.urls import path
from .views import PlanListAPIView, SubscribeAPIView, CommunitySubscriptionsAPIView, UnsubscribeAPIView

urlpatterns = [
    path("<str:IDcommunity>/plans/", PlanListAPIView.as_view(), name="list-plans"),  # Listar planes
    path("<str:IDcommunity>/subscribe/", SubscribeAPIView.as_view(), name="subscribe"),  # Crear suscripción
    path("<str:IDcommunity>/", CommunitySubscriptionsAPIView.as_view(), name="list-subscriptions"),  # Listar suscripciones de una comunidad
    path("<str:IDcommunity>/unsubscribe/<uuid:subscription_id>/", UnsubscribeAPIView.as_view(), name="unsubscribe"),  # Cancelar suscripción
]
