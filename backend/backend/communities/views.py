from django.shortcuts import get_object_or_404, render

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import pandas as pd
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction

from .models import Community, PersonCommunity, UserCommunityRole, Role
from .serializers import CommunitySerializer, PersonCommunitySerializer, UserCommunityRoleSerializer, CommunityDetailSerializer, UserCommunityRoleSerializerTest
from properties.serializers import PropertySerializer

from members.serializers import UserRegistrationSerializer
from members.decorators import community_admin_required

### Comunity management views ###
class CommunityListAPIView(generics.ListAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer


class CommunityUserListAPIView(generics.ListAPIView): #Returns the list of the communities linked with the user, using the CommunityDetailSerializer
    serializer_class = CommunityDetailSerializer

    def get(self, request):
        com_data = {}
        user = request.user
        user_communities = UserCommunityRole.objects.filter(user=user).select_related('community')
        communities_data = []
        for user_community in user_communities:
            community = user_community.community
            community_data = CommunityDetailSerializer(community).data
            
            roles = user_community.roles.all()  # Añadir los roles del usuario
            role_names = [role.name for role in roles]  
            
            community_data['roles'] = role_names

            communities_data.append(community_data)

        com_data['communities'] = communities_data
        return Response(com_data) 


class CommunityCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Crea una nueva comunidad y asigna al usuario actual como administrador.",
        request_body=CommunitySerializer,
        responses={
            status.HTTP_201_CREATED: CommunitySerializer,
            status.HTTP_400_BAD_REQUEST: 'Bad Request'
        }
    )

    def post(self, request):
        user = request.user
        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid():
            community = serializer.save(main_contact_user=user)

            # Obtener el rol de administrador
            admin_role = Role.objects.get(name='admin')

            # Asignar el rol de administrador al usuario en la comunidad recién creada
            user_community_role = UserCommunityRole.objects.create(
                user=user,
                community=community
            )

            # Asignar el rol al usuario
            user_community_role.roles.add(admin_role)
            user_community_role.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_description="Obtiene los detalles de una comunidad específica por ID.",
    responses={
        200: CommunityDetailSerializer,
        404: openapi.Response('Comunidad no encontrada')
    }
)
@api_view(['GET'])
def community_detail(request, IDcommunity):
    if request.method == 'GET':
        try:
            community = Community.objects.get(community_id=IDcommunity)
            serializer = CommunityDetailSerializer(community)
            return Response(serializer.data)
        except Community.DoesNotExist:
            return Response({'error': 'Comunidad no encontrada'}, status=404)
 

@swagger_auto_schema(
    method='put',
    operation_description="Actualiza los detalles de una comunidad específica por ID.",
    request_body=CommunitySerializer,
    responses={
        200: CommunitySerializer,
        400: openapi.Response('Datos inválidos'),
        404: openapi.Response('Comunidad no encontrada')
    }
)
@api_view(['PUT'])
def community_update(request, IDcommunity):
    community = get_object_or_404(Community, community_id=IDcommunity)
    
    serializer = CommunitySerializer(community, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommunityDeleteAPIView(APIView):
    def delete(self, request, IDcommunity):
        community = get_object_or_404(Community, community_id=IDcommunity)
        community.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


### User managemente views ###

class AddUserToCommunityAPIView(APIView):
    def post(self, request, IDcommunity):
        # Registro de usuario
        user_serializer = UserRegistrationSerializer(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()

            # Asignar rol en la comunidad
            community = get_object_or_404(Community, pk=IDcommunity)
            role_data = {
                'user': user.id,
                'community': community.IDcommunity,
                'role': request.data.get('role')
            }
            role_serializer = UserCommunityRoleSerializer(data=role_data)
            if role_serializer.is_valid():
                role_serializer.save()
                return Response({
                    'user': user_serializer.data,
                    'role': role_serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                # Si la creación del rol falla, eliminar usuario creado
                user.delete()
                return Response(role_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CommunityUsersAPIView(APIView):
    def get(self, request, IDcommunity):
        community_roles = UserCommunityRole.objects.filter(community_id=IDcommunity)
        serializer = UserCommunityRoleSerializer(community_roles, many=True)
        return Response(serializer.data)


class CommunityUserRolesAPIView(APIView):
    def get(self, request, IDcommunity):
        # Obtén todos los roles de usuario para la comunidad dada
        roles = UserCommunityRole.objects.filter(community_id=IDcommunity)
        serializer = UserCommunityRoleSerializerTest(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    


class ManageUserCommunityRoleAPIView(APIView):
    
    def post(self, request, IDcommunity):
        # Asegurar que la comunidad exista
        community = get_object_or_404(Community, pk=IDcommunity)
        request.data['community'] = community.IDcommunity
        
        # Crear un nuevo rol
        serializer = UserCommunityRoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, IDcommunity, role_id):
        # Actualizar un rol existente
        role = get_object_or_404(UserCommunityRole, pk=role_id, community_id=IDcommunity)
        serializer = UserCommunityRoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, IDcommunity, role_id):
        # Eliminar un rol existente
        role = get_object_or_404(UserCommunityRole, pk=role_id, community_id=IDcommunity)
        role.delete()
        return Response({'message': 'Rol eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)


class ManageUserRolesAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Gestiona los roles de un vecino en la comunidad.",
        responses={
            200: 'ok',
            404: 'El vecino no existe en la comunidad.',
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'roles_to_add': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description='Lista de roles a añadir'),
                'roles_to_remove': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description='Lista de roles a eliminar'),
            },
            required=[],
        ),
    )
        
    def post(self, request, IDcommunity, neighbour_id):
        # Asegurar que la comunidad exista
        community = get_object_or_404(Community, pk=IDcommunity)
        
        # Buscar el UserCommunityRole existente
        try:
            user_community_role = UserCommunityRole.objects.get(community=community, neighbour_id=neighbour_id)
        except UserCommunityRole.DoesNotExist:
            return Response({"error": "El vecino no existe en la comunidad."}, status=status.HTTP_404_NOT_FOUND)
        
        roles_to_add = request.data.get('roles_to_add', [])
        roles_to_remove = request.data.get('roles_to_remove', [])
        
        # Agregar roles
        if roles_to_add:
            roles = Role.objects.filter(name__in=roles_to_add)
            user_community_role.roles.add(*roles)

        # Eliminar roles
        if roles_to_remove:
            roles = Role.objects.filter(name__in=roles_to_remove)
            user_community_role.roles.remove(*roles)
        
        user_community_role.save()
        return Response(status=status.HTTP_200_OK)


### Neighbour management views ###

class BulkPersonCommunityUploadAPIView(APIView):
    def post(self, request, IDcommunity):
        community = get_object_or_404(Community, community_id=IDcommunity)

        # Verificar si se ha subido un archivo
        if 'file' not in request.FILES:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']

        # Leer el archivo usando pandas
        try:
            df = pd.read_excel(file)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Validar las columnas esperadas en el archivo Excel
        expected_columns = [
            'email', 'name', 'surnames', 'birthdate', 'address', 'phone_number', 
            'personal_id_number', 'personal_id_type', 'role'
        ]
        
        if not all(col in df.columns for col in expected_columns):
            return Response({"error": "Invalid Excel format. Columns do not match."}, status=status.HTTP_400_BAD_REQUEST)

        # Procesar cada fila del archivo y crear la persona correspondiente
        for _, row in df.iterrows():
            try:
                # Obtener el último person_id y asignar el siguiente
                last_person = PersonCommunity.objects.filter(community=community).order_by('person_id').last()
                if last_person:
                    next_person_id = last_person.person_id + 1
                else:
                    next_person_id = 1

                # Crear la instancia de `PersonCommunity` y asignar el person_id manualmente
                person = PersonCommunity.objects.create(
                    community=community,
                    person_id=next_person_id,
                    email=row['email'],
                    name=row['name'],
                    surnames=row['surnames'],
                    birthdate=row['birthdate'],
                    address=row['address'],
                    phone_number=row['phone_number'],
                    personal_id_number=row['personal_id_number'],
                    personal_id_type=row['personal_id_type']
                )

                # Crear el rol para la persona recién creada
                UserCommunityRole.objects.create(
                    community=community,
                    person=person,
                    role=row['role'],
                    user_status='not_registered'
                )

            except Exception as e:
                return Response({"error": f"Error creating person or role: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Persons and roles uploaded successfully"}, status=status.HTTP_201_CREATED)


class PersonCommunityListAPIView(generics.ListCreateAPIView):
    serializer_class = PersonCommunitySerializer

    def get_queryset(self):
        IDcommunity = self.kwargs['IDcommunity']
        return PersonCommunity.objects.filter(community_id=IDcommunity)


class PersonCommunityCreateAPIView(APIView):
    def post(self, request, IDcommunity):
        data = request.data.copy()
        community = get_object_or_404(Community, community_id=IDcommunity) 
        data['community'] = community.community_id  # Asigna el ID de la comunidad directamente
        
        # Calcular el siguiente person_id secuencial para la comunidad
        last_person = PersonCommunity.objects.filter(community=community).order_by('person_id').last()
        if last_person:
            data['person_id'] = last_person.person_id + 1
        else:
            data['person_id'] = 1

        serializer = PersonCommunitySerializer(data=data)
        if serializer.is_valid():
            person = serializer.save()  # Guarda la instancia de PersonCommunity

            # Crear UserCommunityRole con Role y User como null
            UserCommunityRole.objects.create(
                user=None,  # Usuario aún no asignado
                person=person,  # Relación con PersonCommunity
                community=community,  # Relación con la comunidad
                role='pending',  # Rol inicial (puede ser "pending" o el que prefieras)
                user_status='temp'  # Estado del usuario (puede ser "temp" o el que prefieras)
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonCommunityDetailAPIView(APIView):
    def get_object(self, IDcommunity, person_id):
        community = get_object_or_404(Community, IDcommunity=IDcommunity)
        return get_object_or_404(PersonCommunity, community=community, person_id=person_id)
    
    def get(self, request, IDcommunity, person_id):
        person = self.get_object(IDcommunity, person_id)
        serializer = PersonCommunitySerializer(person)
        return Response(serializer.data)
    
    def put(self, request, IDcommunity, person_id):
        person = self.get_object(IDcommunity, person_id)
        serializer = PersonCommunitySerializer(person, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, IDcommunity, person_id):
        person = self.get_object(IDcommunity, person_id)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


