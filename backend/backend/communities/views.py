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

from .models import Community, PersonCommunity, Role
from .serializers import CommunitySerializer, PersonCommunitySerializer, CommunityDetailSerializer, PersonCommunityNeighborsSerializer
from properties.serializers import PropertySerializer

from members.serializers import UserRegistrationSerializer
from members.decorators import community_admin_required

class CommunityCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Crear una nueva comunidad",
        request_body=CommunitySerializer,
        responses={
            201: openapi.Response('Comunidad creada exitosamente', CommunitySerializer),
            400: 'Solicitud inválida',
        }
    )
    def post(self, request):
        # Obtener el usuario autenticado que será el contacto principal de la comunidad
        user = request.user
        
        # Serialización de la comunidad con los datos proporcionados en el cuerpo de la solicitud
        serializer = CommunitySerializer(data=request.data)
        
        # Validación de los datos proporcionados
        if serializer.is_valid():
            # Crear la comunidad con el usuario como contacto principal
            community = serializer.save(main_contact_user=user)

            # Crear el PersonCommunity para el usuario creador
            person = PersonCommunity.objects.create(
                community=community,
                user=user,
                name=user.name,
                surnames=user.surnames,
                email=user.email,
                user_status='active'
            )

            # Asignar el rol de administrador al PersonCommunity
            admin_role = Role.objects.get(name='admin')
            person.roles.add(admin_role)

            # Guardar el PersonCommunity con los roles asignados
            person.save()

            # Retornar la respuesta de éxito con los datos de la comunidad creada
            return Response(CommunitySerializer(community).data, status=status.HTTP_201_CREATED)
        
        # Retornar errores de validación si los datos no son válidos
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
    

#NEIGHBORS = PERSONCOMMUNITY VIEWS

class ListPersonCommunityAPIView(generics.ListAPIView):
    serializer_class = PersonCommunitySerializer

    def get(self, request, IDcommunity, *args, **kwargs):
        # Obtener la comunidad
        community = get_object_or_404(Community, community_id=IDcommunity)
        # Obtener el listado de personas asociadas a esa comunidad
        neighbors = PersonCommunity.objects.filter(community=community)
        serializer = self.serializer_class(neighbors, many=True)
        return Response(serializer.data)

class AddMultiplePersonCommunityAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Añade múltiples personas (PersonCommunity) a una comunidad.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'profiles': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'user': openapi.Schema(type=openapi.TYPE_STRING, description="ID del usuario, si aplica."),
                            'email': openapi.Schema(type=openapi.TYPE_STRING, description="Correo electrónico de la persona."),
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description="Nombre de la persona."),
                            'surnames': openapi.Schema(type=openapi.TYPE_STRING, description="Apellidos de la persona."),
                            'birthdate': openapi.Schema(type=openapi.FORMAT_DATE, description="Fecha de nacimiento."),
                            'address': openapi.Schema(type=openapi.TYPE_STRING, description="Dirección postal."),
                            'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description="Número de teléfono."),
                            'personal_id_number': openapi.Schema(type=openapi.TYPE_STRING, description="Número de identificación personal (DNI, NIE, pasaporte)."),
                            'personal_id_type': openapi.Schema(
                                type=openapi.TYPE_STRING,
                                description="Tipo de documento de identificación.",
                                enum=['DNI', 'NIE', 'PASSPORT']
                            ),
                            'roles': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(type=openapi.TYPE_STRING),
                                description="Lista de roles que se asignarán a la persona (ej: 'admin', 'tenant', 'owner')."
                            )
                        },
                        required=['name', 'surnames']  # Campos obligatorios
                    ),
                    description="Lista de perfiles (personas) que se desean añadir a la comunidad."
                )
            }
        ),
        responses={
            201: openapi.Response(description="Perfiles creados exitosamente."),
            400: openapi.Response(description="Error en los datos proporcionados."),
        }
    )

    def post(self, request, IDcommunity):
        community = get_object_or_404(Community, community_id=IDcommunity)
        
        profiles_data = request.data.get('profiles', [])
        
        if not profiles_data:
            return Response({'error': 'No profiles provided'}, status=status.HTTP_400_BAD_REQUEST)

        created_profiles = []

        for profile_data in profiles_data:
            profile_data['community'] = community.pk  # Set the community for each profile
            
            # If the profile includes a user ID, retrieve the user
            user = None
            if 'user' in profile_data:
                user = get_object_or_404('members.User', pk=profile_data['user'])
                profile_data['user'] = user.pk  # Ensure the user is set properly
            
            serializer = PersonCommunitySerializer(data=profile_data)
            
            if serializer.is_valid():
                person = serializer.save(community=community, user=user)
                
                # Add roles to the person if specified
                roles_to_add = profile_data.get('roles', [])
                if roles_to_add:
                    for role in roles_to_add:
                        role_obj = get_object_or_404(Role, name=role)
                        person.roles.add(role_obj)

                created_profiles.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'created_profiles': created_profiles}, status=status.HTTP_201_CREATED)
    

@api_view(['GET'])
def get_person_community(request, IDcommunity, person_id):
    person = get_object_or_404(PersonCommunity, community_id=IDcommunity, person_id=person_id)
    serializer = PersonCommunitySerializer(person)
    return Response(serializer.data)

@api_view(['PUT'])
def update_person_community(request, IDcommunity, person_id):
    # Obtener la persona de la comunidad
    person = get_object_or_404(PersonCommunity, community_id=IDcommunity, person_id=person_id)
    
    # Obtener los datos enviados en la solicitud
    data = request.data.copy()
    
    # Actualizar los datos del perfil de la persona
    serializer = PersonCommunitySerializer(person, data=data, partial=(request.method == 'PATCH'))
    
    if serializer.is_valid():
        # Guardar los cambios en los datos de la persona
        serializer.save()

        # Gestionar los roles que se añaden
        roles_to_add = data.get('roles', [])
        if roles_to_add:
            for role in roles_to_add:
                role_obj = get_object_or_404(Role, name=role)
                person.roles.add(role_obj)  # Añadir el rol a la persona

        # Gestionar los roles que se eliminan (si es necesario)
        roles_to_remove = data.get('roles_to_remove', [])
        if roles_to_remove:
            for role in roles_to_remove:
                role_obj = get_object_or_404(Role, name=role)
                person.roles.remove(role_obj)  # Eliminar el rol de la persona

        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_person_community(request, IDcommunity, person_id):
    person = get_object_or_404(PersonCommunity, community_id=IDcommunity, person_id=person_id)
    person.delete()
    return Response({'message': 'PersonCommunity eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)