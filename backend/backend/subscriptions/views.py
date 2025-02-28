from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Plan, Subscription
from communities.models import Community
from .serializers import PlanSerializer, SubscriptionSerializer


class PlanListAPIView(generics.ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

    @swagger_auto_schema(
        operation_description="Obtiene la lista de planes de suscripción disponibles.",
        responses={200: PlanSerializer(many=True)}
    )
    def get(self, request):
        return super().get(request)



class SubscribeAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Suscribe una comunidad a un plan.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['plan_id'],
            properties={
                'plan_id': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID, description="ID del plan al que suscribirse")
            }
        ),
        responses={
            201: SubscriptionSerializer(),
            400: "Error en la solicitud"
        }
    )
    def post(self, request, IDcommunity):
        community = get_object_or_404(Community, community_id=IDcommunity)
        plan_id = request.data.get("plan_id")

        if not plan_id:
            return Response({"error": "Se requiere el plan_id"}, status=status.HTTP_400_BAD_REQUEST)

        plan = get_object_or_404(Plan, id=plan_id)

        # Verificar si ya existe una suscripción activa a ese plan
        if Subscription.objects.filter(community=community, plan=plan, is_active=True).exists():
            return Response({"error": "La comunidad ya está suscrita a este plan."}, status=status.HTTP_400_BAD_REQUEST)

        # Crear la suscripción
        subscription = Subscription.objects.create(
            community=community,
            plan=plan
        )

        return Response(SubscriptionSerializer(subscription).data, status=status.HTTP_201_CREATED)



class CommunitySubscriptionsAPIView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer

    @swagger_auto_schema(
        operation_description="Lista las suscripciones activas de una comunidad.",
        responses={200: SubscriptionSerializer(many=True)}
    )
    def get_queryset(self):
        IDcommunity = self.kwargs['IDcommunity']
        return Subscription.objects.filter(community__community_id=IDcommunity, is_active=True)



class UnsubscribeAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Cancela una suscripción de una comunidad.",
        responses={204: "Suscripción cancelada correctamente", 404: "No encontrada"}
    )
    def delete(self, request, IDcommunity, subscription_id):
        community = get_object_or_404(Community, community_id=IDcommunity)
        subscription = get_object_or_404(Subscription, id=subscription_id, community=community, is_active=True)

        # Marcar la suscripción como inactiva
        subscription.is_active = False
        subscription.save()

        return Response({"message": "Suscripción cancelada correctamente."}, status=status.HTTP_204_NO_CONTENT)
