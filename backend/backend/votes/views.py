from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from members.models import User
from .models import Vote, Option, VoteRecord
from .serializers import VoteSerializer, OptionSerializer, VoteRecordSerializer
from django.shortcuts import get_object_or_404

# Vote Views
class VoteCreateAPIView(generics.CreateAPIView):
    serializer_class = VoteSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, community_id=self.kwargs['IDcommunity'])

class VoteListAPIView(generics.ListAPIView):
    serializer_class = VoteSerializer

    def get_queryset(self):
        return Vote.objects.filter(community_id=self.kwargs['IDcommunity'])

class VoteDetailAPIView(generics.RetrieveAPIView):
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()
    lookup_url_kwarg = 'vote_id'

    def get_queryset(self):
        return Vote.objects.filter(community_id=self.kwargs['IDcommunity'])

class VoteUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()
    lookup_url_kwarg = 'vote_id'

    def get_queryset(self):
        return Vote.objects.filter(community_id=self.kwargs['IDcommunity'])

# Option Views
class OptionCreateAPIView(generics.CreateAPIView):
    serializer_class = OptionSerializer

    def perform_create(self, serializer):
        vote = get_object_or_404(Vote, pk=self.kwargs['vote_id'])
        serializer.save(vote=vote, vote_id=self.kwargs['vote_id'])

class OptionListAPIView(generics.ListAPIView):
    serializer_class = OptionSerializer

    def get_queryset(self):
        return Option.objects.filter(vote_id=self.kwargs['vote_id'])

class OptionDetailAPIView(generics.RetrieveAPIView):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()
    lookup_url_kwarg = 'option_id'

    def get_queryset(self):
        return Option.objects.filter(vote_id=self.kwargs['vote_id'])

class OptionUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OptionSerializer
    queryset = Option.objects.all()
    lookup_url_kwarg = 'option_id'

    def get_queryset(self):
        return Option.objects.filter(vote_id=self.kwargs['vote_id'])

# VoteRecord Views
class VoteRecordCreateAPIView(generics.CreateAPIView):
    serializer_class = VoteRecordSerializer

    def perform_create(self, serializer):
        vote = get_object_or_404(Vote, pk=self.kwargs['vote_id'])
        user = get_object_or_404(User, pk=self.request.data.get('user'))
        serializer.save(vote=vote, user=user, recorded_by=self.request.user)

class VoteRecordListAPIView(generics.ListAPIView):
    serializer_class = VoteRecordSerializer

    def get_queryset(self):
        return VoteRecord.objects.filter(vote_id=self.kwargs['vote_id'])
