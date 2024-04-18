from django.shortcuts import render
from django.views import View

from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view


from .serializers import UserRegistrationSerializer, UserSerializer, UserLoginSerializer
from .models import User
from communities.models import Community
from communities.serializers import CommunitySerializer


@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationAPIView(APIView):
    def post(self, request):
        print("Received POST request to register user.")
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
    


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(require_POST, name='dispatch')
class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        print(f'Email: {email}')
        print(f'Password: {password}')
        user1 = User.objects.filter(email=email).first()
        if user1 is not None:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                # Usuario autenticado correctamente
                print('User autenticado')

                login(request, user)
                # Crear una sesión para el usuario
                request.session.create()
                print('Sesion creada')

                return JsonResponse({'success': True})
        print('Credenciales invalidas')

        return JsonResponse({'success': False, 'error': 'Credenciales inválidas'})
  
from rest_framework.permissions import AllowAny


class UserLogoutAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print(f'Sesión actual antes del cierre: {request.session.items()}')
        print(f'Usuario actual antes del cierre: {request.user.email if request.user.is_authenticated else None}')
        request.session.flush()
        username = None
        if request.user.is_authenticated:
            username = request.user.email
        print(f'Usuario cerrado: {username}')
        return Response({
            'message': f'Cierre de sesión exitoso para el usuario {username}',
            'username': username,
            'logged_out': True
        }, status=status.HTTP_200_OK)

    
@login_required
def check_auth_status(request):
    return JsonResponse({'is_authenticated': True})


@api_view(['GET'])
def get_user_email(request):
    if request.user.is_authenticated:
        user_email = request.user.email
        return Response({'email': user_email})
    else:
        return Response({'error': 'Usuario no autenticado'}, status=401)