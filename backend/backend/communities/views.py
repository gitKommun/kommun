from django.shortcuts import render
from rest_framework import generics
from .models import Community
from .serializers import CommunitySerializer

class CommunityListAPIView(generics.ListAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer