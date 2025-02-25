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
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from .serializers import UserRegistrationSerializer, UserSerializer, UserLoginSerializer, UserUpdateSerializer
from .models import User
from communities.models import Community, PersonCommunity, Role
from communities.serializers import CommunitySerializer
from properties.models import Property, PropertyRelationship

class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'user': serializer.data,
            }, status=status.HTTP_201_CREATED)

            #TODO: Validacion email !cubrir casos de uso de suplantación de email
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
      

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(require_POST, name='dispatch')
class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user1 = User.objects.filter(email=email).first()
        if user1 is not None:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                # Usuario autenticado correctamente
                login(request, user)
                # Crear una sesión para el usuario
                request.session.create()

                response_data = {
                    'sessionid': request.session.session_key,
                }

                response = JsonResponse(response_data)
                response.set_cookie('sessionid', request.session.session_key)

                return response

        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


@method_decorator(csrf_exempt, name='dispatch')
class UserLogoutAPIView(APIView):
    def post(self, request):
        #print(f'Sesión actual antes del cierre: {request.session.items()}')
        #print(f'Usuario actual antes del cierre: {request.user.email if request.user.is_authenticated else None}')
        request.session.flush()
        username = None
        if request.user.is_authenticated:
            username = request.user.email
        #print(f'Usuario cerrado: {username}')
        return Response({
            'message': f'Cierre de sesión exitoso para el usuario {username}',
            'username': username,
            'logged_out': True
        }, status=status.HTTP_200_OK)

    
@login_required
def check_auth_status(request):
    return JsonResponse({'is_authenticated': True})




@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description="User data retrieved successfully",
            examples={
                "application/json": {
                    "email": "user@example.com",
                    "name": "John",
                    "surnames": "Doe",
                    "language_config": "en",
                    #"date_joined": "2023-01-01T00:00:00Z",
                    "birthdate": "1990-12-31",
                    "address": "123 Main St",
                    "phone_number": "1234567890",
                    "personal_id_number": "A1234567",
                    "personal_id_type": "Passport",
                    "current_community": {
                        "community_id": 1,
                        "community_name": "Community Name",
                        "community_person_id": 1,
                        "community_user_status": "active",
                        "community_roles": ["owner", "admin"]
                    },
                    "available_communities": [
                        {
                            "community_id": 1,
                            "community_name": "Community Name",
                            "properties": [
                                {
                                    "property_id": 1,
                                    "address": "123 Main St",
                                    "type": "Apartment"
                                }
                            ]
                        }
                    ]
                }
            }
        ),
        401: openapi.Response(
            description="User not authenticated",
            examples={
                "application/json": {
                    "error": "Usuario no autenticado"
                }
            }
        )
    }
)
@api_view(['GET'])
def get_user_data(request):
    if request.user.is_authenticated:
        user = request.user
        user_data = {
            'email': user.email,
            'name': user.name,
            'surnames': user.surnames,
    
            'language_config': user.language_config,
            #'date_joined': user.date_joined
        }


        # Verificar si hay PersonCommunity con el mismo email del usuario en cualquier comunidad
        for person in PersonCommunity.objects.filter(email=user.email, user__isnull=True):
            # Asignar el nombre que ha elegido el usuario en el registro
            if user.name: person.name = user.name
            if user.surnames: person.surnames = user.surnames
            # Asignar el usuario a la instancia de PersonCommunity
            person.user = user
            person.save()

        user_communities = PersonCommunity.objects.filter(user=user).select_related('community')
        user_communities_data = []
        user_current_community = user.current_community if user.current_community else None

        user_current_community_data = {}

        if not user.current_community:
         if user_communities:
             user.current_community = user_communities.first().community
             

        if user.current_community:
            person_community = user_communities.filter(community=user.current_community).first()
            if person_community:
                # Obtener los nombres de los roles
                roles = person_community.roles.all()
                roles_names = [role.name for role in roles]

                birthdate = person_community.birthdate
                adress = person_community.address
                phone_number = person_community.phone_number
                personal_id_number = person_community.personal_id_number
                personal_id_type = person_community.personal_id_type

                user_data['birthdate'] = birthdate.strftime('%Y-%m-%d') if birthdate else None
                user_data['address'] = adress
                user_data['phone_number'] = phone_number
                user_data['personal_id_number'] = personal_id_number
                user_data['personal_id_type'] = personal_id_type

            user_current_community_data = {
                'community_id': user.current_community.community_id,
                'community_name': user.current_community.name,
                'community_person_id': person_community.person_id if person_community else None,
                'community_user_status': person_community.user_status,
                'community_roles': roles_names  # Devolver los nombres de los roles
                
            }

        user_data['current_community'] = user_current_community_data

        for user_community in user_communities:
            community = user_community.community
            # Obtener las propiedades relacionadas con este perfil en cada comunidad
            properties = PropertyRelationship.objects.filter(person=user_community, community=community).select_related('property')
            properties_data = [
                {
                    'property_id': property.property.property_id,
                    'address': property.property.address_complete,
                    'type': property.type,
                }
                for property in properties
            ]


            user_community_data = {
                'community_id': community.community_id,
                'community_name': community.name,
                #'role': user_community.role,
                'properties': properties_data
            }
            user_communities_data.append(user_community_data)

        user_data['available_communities'] = user_communities_data

        return Response(user_data)
    else:
        return Response({'error': 'Usuario no autenticado'}, status=401)
    

class UserUpdateAPIView(APIView):
    """
    Permite actualizar los datos del usuario autenticado.
    
    **Nota:**  
    - Los datos de contacto del usuario (`email`, `name`, `surnames`, `birthdate`, `address`,  
      `phone_number`, `personal_id_number`, `personal_id_type`) se actualizarán automáticamente  
      en todas las instancias de `PersonCommunity` relacionadas con este usuario.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(   
        request_body=UserUpdateSerializer,
        responses={
            200: openapi.Response(
                description="User and related PersonCommunity objects updated successfully",
                examples={
                    "application/json": {
                        "email": "user@example.com",
                        "name": "John",
                        "surnames": "Doe",
                        "birthdate": "1990-12-31",
                        "address": "123 Main St",
                        "phone_number": "1234567890",
                        "personal_id_number": "A1234567",
                        "personal_id_type": "Passport"
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid data",
                examples={
                    "application/json": {
                        "error": "Invalid data"
                    }
                }
            )
        }
    )
    def put(self, request):
        user = self.get_object()
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Update related PersonCommunity objects
            person_communities = PersonCommunity.objects.filter(user=user)
            for person_community in person_communities:
                person_community.email = user.email
                person_community.name = user.name
                person_community.surnames = user.surnames
                person_community.birthdate = request.data.get('birthdate', person_community.birthdate)
                person_community.address = request.data.get('address', person_community.address)
                person_community.phone_number = request.data.get('phone_number', person_community.phone_number)
                person_community.personal_id_number = request.data.get('personal_id_number', person_community.personal_id_number)
                person_community.personal_id_type = request.data.get('personal_id_type', person_community.personal_id_type)
                person_community.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

