from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Claim, Community, ClaimComment, ClaimStatusRecord
from .serializers import ClaimCommentSerializer, ClaimSerializer, ClaimDetailSerializer

class ClaimCreateAPIView(generics.CreateAPIView):
    serializer_class = ClaimSerializer

    def perform_create(self, serializer):
        community = get_object_or_404(Community, IDcommunity=self.kwargs['IDcommunity'])
        serializer.save(user=self.request.user, community=community, status='reported')

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(response.data, status=status.HTTP_201_CREATED)

class ClaimDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ClaimDetailSerializer

    def get_queryset(self):
        community = get_object_or_404(Community, IDcommunity=self.kwargs['IDcommunity'])
        return Claim.objects.filter(community=community)

class ClaimListAPIView(generics.ListAPIView):
    serializer_class = ClaimSerializer

    def get_queryset(self):
        community = get_object_or_404(Community, IDcommunity=self.kwargs['IDcommunity'])
        return Claim.objects.filter(community=community)
    

class ClaimCommentCreateAPIView(generics.CreateAPIView):
    serializer_class = ClaimCommentSerializer

    def perform_create(self, serializer):
        claim = get_object_or_404(Claim, id=self.kwargs['claim_id'])
        serializer.save(user=self.request.user, claim=claim)

class ClaimUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ClaimSerializer

    def get_queryset(self):
        community = get_object_or_404(Community, IDcommunity=self.kwargs['IDcommunity'])
        return Claim.objects.filter(community=community)

    def perform_update(self, serializer):
        claim = self.get_object()
        new_status = serializer.validated_data.get('status', claim.status)
        if claim.status != new_status:
            ClaimStatusRecord.objects.create(claim=claim, status=new_status, changed_by=self.request.user)
        serializer.save()

