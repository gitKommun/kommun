from django.shortcuts import get_object_or_404, render

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import Community, PersonCommunity, Property, UserCommunityRole
from .serializers import CommunitySerializer, PersonCommunitySerializer, PropertySerializer, UserCommunityRoleSerializer

from members.serializers import UserRegistrationSerializer
from members.decorators import community_admin_required

### Comunity management views ###

class CommunityListAPIView(generics.ListAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer


class CommunityCreateAPIView(APIView):
    def post(self, request):
        user = request.user
        serializer = CommunitySerializer(data=request.data)
        if serializer.is_valid():
            community = serializer.save(mainUser=user)

            # Asignar el rol de administrador al usuario en la comunidad recien creada
            UserCommunityRole.objects.create(
                user=user,
                community=community,
                role='admin'
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def community_detail(request, IDcommunity):
    if request.method == 'GET':
        try:
            community = Community.objects.get(IDcommunity=IDcommunity)
            serializer = CommunitySerializer(community)
            return Response(serializer.data)
        except Community.DoesNotExist:
            return Response({'error': 'Comunidad no encontrada'}, status=404)
        
@api_view(['GET', 'PUT', 'PATCH'])
def community_update(request, IDcommunity):
    try:
        community = Community.objects.get(IDcommunity=IDcommunity)
    except Community.DoesNotExist:
        return Response({'error': 'Comunidad no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CommunitySerializer(community)
        return Response(serializer.data)
    
    elif request.method in ['PUT', 'PATCH']:
        serializer = CommunitySerializer(community, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommunityDeleteAPIView(APIView):
    def delete(self, request, IDcommunity):
        community = get_object_or_404(Community, IDcommunity=IDcommunity)
        community.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

### Property managemente views ###

@api_view(['GET'])
def list_properties(request, IDcommunity):
    community = get_object_or_404(Community, IDcommunity=IDcommunity)
    properties = Property.objects.filter(community=community)
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)

#BORRAR: antigua version no segura, permite asignar manualmente el communityID
@api_view(['POST'])
@community_admin_required
def add_property_to_community(request, IDcommunity):
    community = get_object_or_404(Community, pk=IDcommunity)

    # Asigna un número secuencial único para esta comunidad
    next_property_number = Property.objects.filter(community=community).count() + 1

    new_property = Property(
        community=community,
        property_id=next_property_number,
        typeProperty=request.data.get('typeProperty'),
        communityPropertyPercentage=request.data.get('communityPropertyPercentage')
    )

    serializer = PropertySerializer(new_property, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
@community_admin_required
def add_property_to_community2(request, IDcommunity):
    community = get_object_or_404(Community, IDcommunity=IDcommunity)

    # Asigna un número secuencial único para esta comunidad
    next_property_number = Property.objects.filter(community=community).count() + 1

    new_property = Property(
        community=community,
        property_id=next_property_number,
        numberProperty=request.data.get('numberProperty'),
        typeProperty=request.data.get('typeProperty'),
        communityPropertyPercentage=request.data.get('communityPropertyPercentage')
    )
    new_property.save()

    return Response(PropertySerializer(new_property).data, status=status.HTTP_201_CREATED)
    

@api_view(['PUT'])
def edit_property(request, IDcommunity, property_id):
    community = get_object_or_404(Community, pk=IDcommunity)
    property_instance = get_object_or_404(Property, community=community, property_id=property_id)

    serializer = PropertySerializer(property_instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_property(request, IDcommunity, property_id):
    community = get_object_or_404(Community, pk=IDcommunity)
    property_instance = get_object_or_404(Property, community=community, property_id=property_id)
    property_instance.delete()
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
    

### Person management views ###


class PersonCommunityListAPIView(generics.ListCreateAPIView):
    serializer_class = PersonCommunitySerializer

    def get_queryset(self):
        IDcommunity = self.kwargs['IDcommunity']
        return PersonCommunity.objects.filter(community_id=IDcommunity)


class PersonCommunityCreateAPIView(APIView):
    def post(self, request, IDcommunity):
        data = request.data.copy()
        data['community'] = IDcommunity
        serializer = PersonCommunitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class PersonCommunityCreateAPIView(APIView):
    def post(self, request, IDcommunity):
        data = request.data.copy()
        community = get_object_or_404(Community, IDcommunity=IDcommunity)
        data['community'] = IDcommunity
        
        # Calcular el siguiente person_id secuencial para la comunidad
        last_person = PersonCommunity.objects.filter(community=community).order_by('person_id').last()
        if last_person:
            data['person_id'] = last_person.person_id + 1
        else:
            data['person_id'] = 1

        serializer = PersonCommunitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

#Detail, update, delete PersonCommunity
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