from backend import settings
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView

from django.shortcuts import get_object_or_404

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import Claim, Community, ClaimComment, ClaimStatusRecord
from .serializers import ClaimCommentSerializer, ClaimSerializer, ClaimDetailSerializer, ClaimTimelineSerializer

from members.views import create_notification
from members.models import User, Notification

#from subscriptions.permissions import HasSubscriptionPermission


class ClaimCreateAPIView(generics.CreateAPIView):
    serializer_class = ClaimSerializer

    def perform_create(self, serializer):
        community = get_object_or_404(Community, community_id=self.kwargs['IDcommunity'])
        claim = serializer.save(created_by=self.request.user, community=community, status='reported')
        
        # Crear notificación para cada admin de la comunidad
        admin_users = User.objects.filter(id__in=community.get_admins_users())
        for admin in admin_users:
            create_notification(
                recipient=admin,
                title="Nueva reclamación",
                message=f"Nueva reclamación {claim.claim_id} {claim.title}, creada por {claim.created_by.name} {claim.created_by.surnames}. Accede a la reclamación para aprobarla o rechazarla.",
                link=f"{settings.FRONTEND_URL}/claims/{community.community_id}/{claim.claim_id}"
            )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_201_CREATED)
    
class ClaimDetailAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Obtener el detalle de una incidencia en una comunidad específica.",
        manual_parameters=[
            openapi.Parameter(
                'IDcommunity',
                openapi.IN_PATH,
                description="ID de la comunidad",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'claim_id',
                openapi.IN_PATH,
                description="ID relativo de la incidencia dentro de la comunidad",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Detalle de la incidencia con historial de cambios y mensajes",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "claim_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID relativo de la incidencia"),
                        "title": openapi.Schema(type=openapi.TYPE_STRING, description="Título de la incidencia"),
                        "description": openapi.Schema(type=openapi.TYPE_STRING, description="Descripción de la incidencia"),
                        "category": openapi.Schema(type=openapi.TYPE_STRING, description="Categoría de la incidencia"),
                        "priority": openapi.Schema(type=openapi.TYPE_STRING, description="Prioridad de la incidencia"),
                        "status": openapi.Schema(type=openapi.TYPE_STRING, description="Estado actual de la incidencia"),
                        "incident_date": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fecha de la incidencia"),
                        "problem_persists": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Indica si el problema persiste"),
                        "created_at": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fecha de creación"),
                        "updated_at": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Última actualización"),
                        "user_fullname": openapi.Schema(type=openapi.TYPE_STRING, description="Nombre completo del usuario que creó la incidencia"),
                        "comments": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            description="Lista de comentarios asociados a la incidencia",
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "comment_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID del comentario"),
                                    "comment": openapi.Schema(type=openapi.TYPE_STRING, description="Texto del comentario"),
                                    "created_at": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fecha de creación del comentario"),
                                    "user_fullname": openapi.Schema(type=openapi.TYPE_STRING, description="Nombre del usuario que comentó")
                                }
                            )
                        ),
                        "timeline": openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            description="Historial de cambios de estado y mensajes relacionados",
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "type": openapi.Schema(type=openapi.TYPE_STRING, description="Tipo de evento ('status_change' o 'message')"),
                                    "timestamp": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fecha del evento"),
                                    "data": openapi.Schema(
                                        type=openapi.TYPE_OBJECT,
                                        properties={
                                            "previous_status": openapi.Schema(type=openapi.TYPE_STRING, description="Estado anterior (solo en 'status_change')"),
                                            "new_status": openapi.Schema(type=openapi.TYPE_STRING, description="Nuevo estado (solo en 'status_change')"),
                                            "message_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="ID del mensaje (solo en 'message')"),
                                            "message_type": openapi.Schema(type=openapi.TYPE_STRING, description="Tipo de mensaje (solo en 'message')"),
                                            "message": openapi.Schema(type=openapi.TYPE_STRING, description="Contenido del mensaje (solo en 'message')"),
                                            "user_fullname": openapi.Schema(type=openapi.TYPE_STRING, description="Nombre del usuario que envió el mensaje (solo en 'message')")
                                        }
                                    )
                                }
                            )
                        )
                    }
                )
            ),
            404: openapi.Response(description="Incidencia no encontrada"),
        }
    )
    def get(self, request, IDcommunity, claim_id):
        # Obtener la incidencia
        claim = get_object_or_404(Claim, community__community_id=IDcommunity, claim_id=claim_id)

        # Obtener comentarios
        comments = ClaimComment.objects.filter(claim=claim).order_by("-created_at")
        comments_data = [
            {
                "comment_id": comment.claim_comment_id,
                "comment": comment.comment,
                "created_at": comment.created_at.strftime("%Y-%m-%dT%H:%M") if comment.created_at else None,
                "user_fullname": f"{comment.user.name} {comment.user.surnames}".strip() if comment.user else None
            }
            for comment in comments
        ]

        # Obtener historial de cambios de estado
        status_changes = claim.status_records.all().order_by("-timestamp")
        timeline_entries = [
            {
                "type": "status_change",
                "timestamp": record.timestamp.strftime("%Y-%m-%dT%H:%M") if record.timestamp else None,
                "data": {
                    "previous_status": status_changes[i + 1].status if i + 1 < len(status_changes) else None,
                    "new_status": record.status
                }
            }
            for i, record in enumerate(status_changes)
        ]

        # Obtener mensajes relacionados
        messages = claim.messages.all().order_by("-created_at")
        timeline_entries += [
            {
                "type": "message",
                "timestamp": message.created_at.strftime("%Y-%m-%dT%H:%M") if message.created_at else None,
                "data": {
                    "message_id": message.message_id,
                    "message_type": message.message_type,
                    "message": message.message,
                    "user_fullname": f"{message.user.name} {message.user.surnames}".strip() if message.user else None
                }
            }
            for message in messages
        ]

        # Ordenar el timeline de más reciente a más antiguo
        timeline_entries.sort(key=lambda x: x["timestamp"] if x["timestamp"] else "", reverse=True)

        # Construcción de la respuesta final
        response_data = {
            "claim_id": claim.claim_id,
            "title": claim.title,
            "description": claim.description,
            "category": claim.category,
            "priority": claim.priority,
            "status": claim.status,
            "incident_date": claim.incident_date.strftime("%Y-%m-%dT%H:%M") if claim.incident_date else None,
            "problem_persists": claim.problem_persists,
            "created_at": claim.created_at.strftime("%Y-%m-%dT%H:%M") if claim.created_at else None,
            "user_fullname": f"{claim.created_by.name} {claim.created_by.surnames}".strip() if claim.created_by else None,
            "updated_at": claim.updated_at.strftime("%Y-%m-%dT%H:%M") if claim.updated_at else None,
            "timeline": timeline_entries,
            "comments": comments_data
        }

        return Response(response_data, status=200)

class ClaimListAPIView(generics.ListAPIView):
    serializer_class = ClaimSerializer
    #permission_classes = [HasSubscriptionPermission]  # Verifica la suscripción

    def get_queryset(self):
        community = get_object_or_404(Community, community_id=self.kwargs['IDcommunity'])
        return Claim.objects.filter(community=community).order_by('-created_at')

class ClaimCommentCreateAPIView(generics.CreateAPIView):
    serializer_class = ClaimCommentSerializer

    def perform_create(self, serializer):
        claim = get_object_or_404(Claim, claim_id=self.kwargs['claim_id'])
        serializer.save(user=self.request.user, claim=claim)

class ClaimUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ClaimSerializer
    lookup_field = 'claim_id'  # Usar claim_id como campo de búsqueda

    def get_queryset(self):
        # Obtener la comunidad usando el ID proporcionado en los parámetros de la URL
        community = get_object_or_404(Community, community_id=self.kwargs['IDcommunity'])
        
        # Filtrar las reclamaciones de la comunidad utilizando el claim_id relativo
        return Claim.objects.filter(community=community)

        
    def perform_update(self, serializer):
        # Obtener el objeto claim actual
        claim = self.get_object()
        
        # Obtener los datos validados del serializer
        validated_data = serializer.validated_data
        print("Datos validados:", validated_data)

        # Obtener el nuevo estado desde los datos validados
        new_status = validated_data.get('status', claim.status)
        print("Nuevo estado:", new_status, "Estado actual:", claim.status)

        # Si el estado cambia, registrar el cambio en ClaimStatusRecord
        if claim.status != new_status:
            ClaimStatusRecord.objects.create(
                claim=claim,
                status=new_status,
                changed_by=self.request.user
            )
            # Asignar el nuevo estado al objeto claim antes de guardar
            claim.status = new_status

            # Crear notificación para el creador de la incidencia
            status_display = dict(Claim.STATUS_CHOICES)[new_status]
            Notification.objects.create(
                recipient=claim.created_by,
                title=f"Actualización de incidencia #{claim.claim_id}",
                message=f"El estado de tu incidencia '{claim.title}' ha cambiado.",
                category="claim_update",
                link=f"/communities/{claim.community.community_id}/claims/{claim.claim_id}"
            )
        
        # Guardar los cambios en el objeto claim
        serializer.save()

class ClaimDeleteAPIView(generics.DestroyAPIView):
    serializer_class = ClaimDetailSerializer  # Opcional si necesitas mostrar datos antes de eliminar
    lookup_field = 'claim_id'

    def get_queryset(self):
        # Obtener la comunidad usando el ID proporcionado en los parámetros de la URL
        community = get_object_or_404(Community, community_id=self.kwargs['IDcommunity'])
        
        # Filtrar las reclamaciones de la comunidad utilizando el claim_id relativo
        return Claim.objects.filter(community=community)
    
class ClaimCommentDeleteAPIView(generics.DestroyAPIView):
    def get_queryset(self):
        # Filtra los comentarios por el `claim` y el `claim_comment_id`
        claim = get_object_or_404(Claim, claim_id=self.kwargs['claim_id'], community__community_id=self.kwargs['IDcommunity'])
        return ClaimComment.objects.filter(claim=claim)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        comment = get_object_or_404(queryset, claim_comment_id=self.kwargs['claim_comment_id'])
        comment.delete()
        return Response({"detail": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)