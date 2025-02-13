from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from .models import Claim, Community, ClaimComment, ClaimStatusRecord
from .serializers import ClaimCommentSerializer, ClaimSerializer, ClaimDetailSerializer

from subscriptions.permissions import HasSubscriptionPermission


class ClaimCreateAPIView(generics.CreateAPIView):
    serializer_class = ClaimSerializer

    def perform_create(self, serializer):
        community = get_object_or_404(Community, community_id=self.kwargs['IDcommunity'])
        serializer.save(user=self.request.user, community=community, status='reported')

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_201_CREATED)

class ClaimDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ClaimDetailSerializer
    lookup_field = 'claim_id'  # Define que el campo a usar es 'claim_id'

    def get_queryset(self):
        # Obtener la comunidad usando el ID proporcionado en los parámetros de la URL
        community = get_object_or_404(Community, community_id=self.kwargs['IDcommunity'])
        
        # Filtrar las reclamaciones de la comunidad utilizando el claim_id relativo
        return Claim.objects.filter(community=community, claim_id=self.kwargs['claim_id'])

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
        print("Datos validados:", validated_data)  # Verifica qué datos se están recibiendo

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