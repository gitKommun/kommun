from django.shortcuts import get_object_or_404, render
from django.db import transaction

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

import pandas as pd

from .models import  Property
from .serializers import  PropertySerializer

from communities.models import Community


# Create your views here.
### Property managemente views ###
@swagger_auto_schema(
    method='get',
    operation_description="Obtiene la lista de propiedades asociadas a una comunidad específica.",
    responses={
        200: PropertySerializer(many=True),
        404: 'Comunidad no encontrada'
    }
)
@api_view(['GET'])
def list_properties(request, IDcommunity):
    community = get_object_or_404(Community, community_id=IDcommunity)
    properties = Property.objects.filter(community=community)
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)


class PropertyCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Crea una nueva propiedad asociada a una comunidad específica.",
        request_body=PropertySerializer,
        responses={
            201: PropertySerializer,
            400: 'Solicitud incorrecta. Los datos proporcionados no son válidos.',
            404: 'Comunidad no encontrada'
        }
    )
    def post(self, request, IDcommunity):
        community = get_object_or_404(Community, community_id=IDcommunity)
        
        data = request.data.copy()
        data['community'] = community.pk  
        
        serializer = PropertySerializer(data=data)
        if serializer.is_valid():
            serializer.save(community=community)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyUpdateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Actualiza una propiedad existente en una comunidad específica.",
        request_body=PropertySerializer,
        responses={
            200: PropertySerializer,
            400: 'Solicitud incorrecta. Los datos proporcionados no son válidos.',
            404: 'Comunidad o propiedad no encontrada'
        }
    )
    def put(self, request, IDcommunity, property_id):
        # Buscar la comunidad y la propiedad
        community = get_object_or_404(Community, community_id=IDcommunity)
        property_instance = get_object_or_404(Property, community=community, property_id=property_id)
        
        # Copiar los datos del request
        data = request.data.copy()
        data['community'] = community.pk  # Asegurar que la comunidad sigue siendo la misma
        
        # Serializar y actualizar la propiedad
        serializer = PropertySerializer(property_instance, data=data, partial=True)
        if serializer.is_valid():
            updated_property = serializer.save()
            return Response(PropertySerializer(updated_property).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyDeleteAPIView(APIView):
    def delete(self, request, IDcommunity, property_id):
        # Buscar la comunidad y la propiedad
        community = get_object_or_404(Community, community_id=IDcommunity)
        property_instance = get_object_or_404(Property, community=community, property_id=property_id)
        
        # Eliminar la propiedad
        property_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BulkUploadPropertiesView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(
        operation_description="Carga masiva de propiedades mediante un archivo Excel.",
        request_body=None,
        responses={
            201: "Las propiedades se han subido exitosamente.",
            400: "Solicitud incorrecta. Error en la carga del archivo o en los datos proporcionados.",
            404: "Comunidad no encontrada."
        }
    )
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
            'property_id', 'surface_area', 'participation_coefficient', 'usage', 'address_complete', 
            'block', 'staircase', 'floor', 'door'
        ]
        
        if not all(col in df.columns for col in expected_columns):
            return Response({"error": "Invalid Excel format. Columns do not match."}, status=status.HTTP_400_BAD_REQUEST)

        # Procesar cada fila del archivo y crear la propiedad correspondiente
        for _, row in df.iterrows():
            try:
                Property.objects.create(
                    community=community,
                    property_id=row['property_id'],
                    surface_area=row['surface_area'],
                    participation_coefficient=row['participation_coefficient'],
                    usage=row['usage'],
                    address_complete=row['address_complete'],
                    block=row['block'],
                    staircase=row['staircase'],
                    floor=row['floor'],
                    door=row['door']
                )
            except Exception as e:
                return Response({"error": f"Error creating property: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Properties uploaded successfully"}, status=status.HTTP_201_CREATED)

