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
import requests

from .models import  Property, PropertyRelationship
from .serializers import  PropertySerializer, PropertyRelationshipSerializer, PropertyDetailSerializer, PropertyOwnerSerializer
from communities.models import Community, PersonCommunity
from communities.serializers import PersonCommunitySerializer
from core.models import Municipality, Province, PostalCode


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
    serializer = PropertyDetailSerializer(properties, many=True)
    return Response(serializer.data)


class ListPropertiesWithOwnerAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Obtener el listado de propiedades con su propietario asociado (owner) en una comunidad específica.",
        responses={
            200: openapi.Response(
                description="Lista de propiedades con el propietario (owner) asociado.",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'property_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID relativo de la propiedad"),
                            'address_complete': openapi.Schema(type=openapi.TYPE_STRING, description="Dirección completa de la propiedad"),
                            'surface_area': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description="Superficie de la propiedad"),
                            'participation_coefficient': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DECIMAL, description="Coeficiente de participación"),
                            'usage': openapi.Schema(type=openapi.TYPE_STRING, description="Uso de la propiedad"),
                            'owner': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'person_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID relativo del perfil en la comunidad"),
                                    'name': openapi.Schema(type=openapi.TYPE_STRING, description="Nombre del propietario"),
                                    'surnames': openapi.Schema(type=openapi.TYPE_STRING, description="Apellidos del propietario"),
                                    'email': openapi.Schema(type=openapi.TYPE_STRING, description="Correo electrónico del propietario"),
                                    'user_status': openapi.Schema(type=openapi.TYPE_STRING, description="Estado del propietario en la comunidad"),
                                    'roles': openapi.Schema(
                                        type=openapi.TYPE_ARRAY,
                                        items=openapi.Schema(type=openapi.TYPE_STRING),
                                        description="Roles asociados al propietario"
                                    )
                                },
                                description="Información del propietario de la propiedad"
                            )
                        }
                    )
                )
            ),
            404: openapi.Response(description="Comunidad no encontrada.")
        }
    )


    def get(self, request, IDcommunity):
        # Obtener todas las propiedades de la comunidad
        properties = Property.objects.filter(community__community_id=IDcommunity)
        properties_data = []

        for property in properties:
            # Buscar el owner de la propiedad
            owner_relationship = PropertyRelationship.objects.filter(property=property, type='owner').first()
            owner_data = None

            if owner_relationship and owner_relationship.person:
                owner_data = PersonCommunitySerializer(owner_relationship.person).data

            # Serializar los datos de la propiedad y agregar el owner
            property_data = PropertyOwnerSerializer(property).data
            property_data['owner'] = owner_data

            properties_data.append(property_data)

        return Response(properties_data, status=status.HTTP_200_OK)


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


class DeleteAllPropertiesAPIView(APIView):
    def delete(self, request, IDcommunity):
        # Obtener la comunidad
        community = get_object_or_404(Community, community_id=IDcommunity)
        
        # Eliminar todas las propiedades asociadas a la comunidad
        properties = Property.objects.filter(community=community)
        count = properties.count()
        properties.delete()
        
        return Response({
            'message': f'Se han eliminado {count} propiedades de la comunidad {community.name}.'
        }, status=status.HTTP_200_OK)

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

class BulkCreatePropertiesFromCatastroAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Crea múltiples propiedades a partir de una lista de referencias catastrales.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ref_catastrales': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description="Lista de referencias catastrales"
                )
            }
        ),
        responses={201: "Propiedades creadas exitosamente.", 400: "Error al procesar la solicitud."}
    )
    
    def post(self, request, IDcommunity):
        # Obtener la comunidad
        community = get_object_or_404(Community, community_id=IDcommunity)
        
        # Obtener la lista de referencias catastrales de la solicitud
        ref_catastrales = request.data.get('ref_catastrales', [])
        if not ref_catastrales or not isinstance(ref_catastrales, list):
            return Response({"error": "Se requiere una lista de referencias catastrales"}, status=status.HTTP_400_BAD_REQUEST)

        created_properties = []
        total_inmuebles_encontrados = 0
        total_propiedades_creadas = 0
        errors = []

        # Procesar cada referencia catastral en la lista
        for ref_catastro in ref_catastrales:
            catastro_api_url = f"http://ovc.catastro.meh.es/OVCServWeb/OVCWcfCallejero/COVCCallejero.svc/json/Consulta_DNPRC?RefCat={ref_catastro}"
            
            # Hacer la solicitud a la API del Catastro
            try:
                response = requests.get(catastro_api_url)
                data = response.json()
            except Exception as e:
                errors.append({"ref_catastro": ref_catastro, "error": f"Error al conectarse con la API del Catastro: {str(e)}"})
                continue

            # Verificar si la API devolvió datos en el formato correcto
            try:
                inmuebles = data['consulta_dnprcResult']['lrcdnp']['rcdnp']  # Extraer la lista de inmuebles
                total_inmuebles_encontrados = data['consulta_dnprcResult']['control']['cudnp']
                if not isinstance(inmuebles, list):
                    inmuebles = [inmuebles]  # Asegurarse de que es una lista de inmuebles, incluso si es uno solo
            except KeyError:
                errors.append({"ref_catastro": ref_catastro, "error": "No se encontraron datos para la referencia catastral proporcionada"})
                continue

           
            # Procesar cada inmueble y crear una propiedad
            for inmueble in inmuebles:
            
                try:
                    address_data = inmueble['dt']['locs']['lous']['lourb']['dir']
                    economic_data = inmueble['debi']
                except KeyError:
                    errors.append({"ref_catastro": ref_catastro, "error": "Datos incompletos en la API del Catastro"})
                    continue

                location_internal = inmueble['dt']['locs']['lous']['lourb']
                #print(location_internal)
                block = location_internal['loint'].get('bq', '')
                staircase = location_internal['loint'].get('es', '')
                floor = location_internal['loint'].get('pt', '')
                door = location_internal['loint'].get('pu', '')

                # Construir address_complete con el formato "Bl: 1 Es: 2 Pl: 3 Pt: 4"
                address_complete = f"{address_data.get('tv', '')} {address_data.get('nv', '')}, {address_data.get('pnp', '')}".strip()
                adress_stret = address_complete

                # Añadir bloque, escalera, planta y puerta solo si existen, y siguiendo el formato del Catastro
                if block:
                    address_complete += f" Bl:{block}"
                if staircase:
                    address_complete += f" Es:{staircase}"
                if floor:
                    address_complete += f" Pl:{floor}"
                if door:
                    address_complete += f" Pt:{door}"

                # Actualizar los datos de la comunidad con la primera referencia catastral
                if total_propiedades_creadas == 1:
                    print("Actualizando los datos de la comunidad con la primera referencia catastral")
                    try:
                        city_code = inmueble['dt']['loine']['cp'] + inmueble['dt']['loine']['cm'].zfill(3)
                        province_code = inmueble['dt']['loine']['cp']
                        postal_code = inmueble['dt']['locs']['lous']['lourb'].get('dp')

                        #print(f"city_code: {city_code}, province_code: {province_code}, postal_code: {postal_code}")

                        # Buscar el municipio y provincia por su código INE
                        try:
                            city = Municipality.objects.get(code_ine=city_code)
                            province = Province.objects.get(code=province_code)

                            print(f"City: {city.name}, Province: {province.name}")

                            # Actualizar los campos de la comunidad
                            community.city = city.name
                            community.province = province
                            community.postal_code = postal_code
                            #community.postal_code = postal_code
                            community.catastral_ref = ref_catastro
                            community.address = adress_stret
                            community.save()
                            #print(f"Community updated: {community.city.name}, {community.province.name}, {community.postal_code}")

                        except Municipality.DoesNotExist:
                            print(f"Municipio con código INE {city_code} no encontrado.")
                            errors.append({"ref_catastro": ref_catastro, "error": "Municipio no encontrado"})
                        except Province.DoesNotExist:
                            print(f"Provincia con código INE {province_code} no encontrada.")
                            errors.append({"ref_catastro": ref_catastro, "error": "Provincia no encontrada"})
                    except KeyError:
                        print("No se encontraron los datos de ubicación de la comunidad en la referencia catastral")
                        errors.append({"ref_catastro": ref_catastro, "error": "No se encontraron los datos de ubicación de la comunidad en la referencia catastral"})

                    print("FIN")

                # Extraer los datos relevantes para cada inmueble
                try:
                    property_data = {
                        'community': community.community_id,
                        'surface_area': economic_data.get('sfc'),
                        'participation_coefficient': float(economic_data.get('cpt').replace(',', '.')),  # Asegurarse de que el formato numérico sea válido .replace(',', '.')
                        'usage': economic_data.get('luso', '').upper(),  # Convierte el uso a mayúsculas para que coincida con las opciones
                        'address_complete': address_complete,
                        'block': block,
                        'staircase': staircase,
                        'floor': floor,
                        'door': door,
                    }

                except KeyError as e:
                    errors.append({"ref_catastro": ref_catastro, "error": f"Datos incompletos en la API del Catastro: {str(e)}"})
                    continue

                # Serializar y crear la propiedad
                #print(property_data)
                serializer = PropertySerializer(data=property_data)
                if serializer.is_valid():
                    created_property = serializer.save(community=community)  # Asociar la propiedad con la comunidad
                    created_properties.append(serializer.data)
                    total_propiedades_creadas += 1
                else:
                    errors.append({"ref_catastro": ref_catastro, "error": serializer.errors})
        
        # Respuesta final con el resumen de la operación
        resumen = {
            "total_inmuebles_encontrados": total_inmuebles_encontrados,
            "total_propiedades_creadas": total_propiedades_creadas,
            "errores": errors
        }

        # Respuesta final con las propiedades creadas y los posibles errores
        if errors:
            return Response({
                "resumen": resumen,
                #"created_properties": created_properties,
                "errors": errors
            }, status=status.HTTP_207_MULTI_STATUS)  # Multi-status para indicar que hubo éxitos y errores

        return Response(resumen, status=status.HTTP_201_CREATED)
    



# Crear relación de propiedad
class CreatePropertyRelationshipAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Crear una relación entre una propiedad y una persona dentro de una comunidad.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['property_id', 'person_id', 'type'],
            properties={
                'property_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la propiedad dentro de la comunidad'),
                'person_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la persona dentro de la comunidad'),
                'type': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de relación (owner o tenant)', enum=['owner', 'tenant']),
            },
        ),
        responses={
            201: 'ok',
            400: 'Bad request',
            404: 'Not found'
        }
    )

    def post(self, request, IDcommunity):
        # Obtener la comunidad de la URL
        community = get_object_or_404(Community, community_id=IDcommunity)
        
        # Obtener los datos de la solicitud
        property_id = request.data.get('property_id')
        person_id = request.data.get('person_id')
        relationship_type = request.data.get('type')

        # Verificar que los datos necesarios estén presentes
        if not property_id or not person_id or not relationship_type:
            return Response({'error': 'property_id, person_id, and type are required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener la instancia de la propiedad
        property_instance = get_object_or_404(Property, community=community, property_id=property_id)

        # Obtener la instancia de la persona (usando el modelo PersonCommunity, no una cadena)
        person_instance = get_object_or_404(PersonCommunity, community=community, person_id=person_id)

        # Crear la relación de propiedad
        relationship_data = {
            'community': community.community_id,
            'property': property_instance.id,
            'person': person_instance.id,
            'type': relationship_type
        }

        serializer = PropertyRelationshipSerializer(data=relationship_data)

        if serializer.is_valid():
            serializer.save()
            return Response("ok", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Eliminar relación de propiedad
class DeletePropertyRelationshipAPIView(APIView):
    
    @swagger_auto_schema(
        operation_description="Eliminar una relación entre una propiedad y una persona dentro de una comunidad.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['property_id', 'person_id', 'type'],
            properties={
                'property_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la propiedad dentro de la comunidad'),
                'person_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la persona dentro de la comunidad'),
                'type': openapi.Schema(type=openapi.TYPE_STRING, description='Tipo de relación (owner o tenant)', enum=['owner', 'tenant']),
            },
        ),
        responses={
            204: 'Deleted successfully',
            400: 'Bad request',
            404: 'Not found'
        }
    )
    def delete(self, request, IDcommunity):
        # Obtener la comunidad de la URL
        community = get_object_or_404(Community, community_id=IDcommunity)
        
        # Obtener los datos de la solicitud
        property_id = request.data.get('property_id')
        person_id = request.data.get('person_id')
        relationship_type = request.data.get('type')

        # Verificar que los datos necesarios estén presentes
        if not property_id or not person_id or not relationship_type:
            return Response({'error': 'property_id, person_id, and type are required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener la instancia de la propiedad
        property_instance = get_object_or_404(Property, community=community, property_id=property_id)

        # Obtener la instancia de la persona
        person_instance = get_object_or_404(PersonCommunity, community=community, person_id=person_id)

        # Obtener la relación de propiedad y eliminarla
        relationship_instance = get_object_or_404(PropertyRelationship, community=community, property=property_instance, person=person_instance, type=relationship_type)
        
        relationship_instance.delete()

        return Response({'message': 'Relationship deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

