from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.contenttypes.models import ContentType

from .serializers import UserRegistrationSerializer, UserSerializer, UserLoginSerializer
from .models import User
from communities.models import Community
from communities.serializers import CommunitySerializer

class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Crea Usuario gestor de comunidad y genera una comunidad en blanco

class UserMainContactCommunityRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            community = Community.objects.create()
            
            # Asignar al usuario como el contacto principal de la comunidad utilizando clave foránea genérica
            community.main_contact_type = ContentType.objects.get_for_model(User)
            community.main_contact_id = user.id
            community.save()
            
            community_serializer = CommunitySerializer(community)
            return Response(community_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    

class UserLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user is not None:
            user = authenticate(request, email=user.email, password=password)
            if user is not None:
                # Usuario autenticado correctamente
                return Response({'message': 'Inicio de sesión exitoso'}, status=status.HTTP_200_OK)
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)