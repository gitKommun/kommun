
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CommonArea, Reservation
from communities.models import Community
from .serializers import CommonAreaSerializer, ReservationSerializer


class CommonAreaCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Crear una nueva zona común en una comunidad específica. "
                              "El `area_id` se asigna automáticamente. Si es reservable, "
                              "se deben indicar la unidad de tiempo y la duración de la reserva. "
                              "Se pueden definir horarios de uso con `usage_start` y `usage_end`.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'reservable'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="Nombre de la zona común"),
                'type': openapi.Schema(type=openapi.TYPE_STRING, description="Tipo de la zona común"),
                'reservable': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Indica si la zona común es reservable"),
                'reservation_duration': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="Duración de la reserva (requerido si es reservable)"
                ),
                'time_unit': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['MIN', 'HOUR', 'DAY'],
                    description="Unidad de tiempo para la duración de la reserva"
                ),
                'usage_start': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Hora de inicio del uso permitido en formato HH:MM:SS (ej. '08:00:00')"
                ),
                'usage_end': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Hora de finalización del uso permitido en formato HH:MM:SS (ej. '22:00:00')"
                ),
            }
        ),
        responses={
            201: openapi.Response(
                description="Zona común creada exitosamente.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'area_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID relativo de la zona común"),
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description="Nombre de la zona común"),
                        'type': openapi.Schema(type=openapi.TYPE_STRING, description="Tipo de la zona común"),
                        'reservable': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Indica si la zona común es reservable"),
                        'reservation_duration': openapi.Schema(type=openapi.TYPE_INTEGER, description="Duración de la reserva"),
                        'time_unit': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=['MIN', 'HOUR', 'DAY'],
                            description="Unidad de tiempo para la duración de la reserva"
                        ),
                        'usage_start': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Hora de inicio del uso permitido en formato HH:MM:SS"
                        ),
                        'usage_end': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Hora de finalización del uso permitido en formato HH:MM:SS"
                        ),
                        'community': openapi.Schema(type=openapi.TYPE_STRING, description="ID de la comunidad asociada"),
                    }
                )
            ),
            400: openapi.Response(description="Error al crear la zona común.")
        }
    )
    def post(self, request, IDcommunity):
        community = get_object_or_404(Community, community_id=IDcommunity)

        data = request.data.copy()
        data['community'] = community.community_id 
        serializer = CommonAreaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class CommonAreaListAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Obtener una lista de todas las zonas comunes en una comunidad específica.",
        responses={
            200: openapi.Response(
                description="Lista de zonas comunes.",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'area_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID de la zona común"),
                            'name': openapi.Schema(type=openapi.TYPE_STRING, description="Nombre de la zona común"),
                            'type': openapi.Schema(type=openapi.TYPE_STRING, description="Tipo de la zona común"),  # Eliminar `required=False`
                            'reservable': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Indica si la zona común es reservable"),
                            'reservation_duration': openapi.Schema(
                                type=openapi.TYPE_INTEGER, 
                                description="Duración de la reserva (requerido si es reservable)"
                            ),
                            'time_unit': openapi.Schema(
                                type=openapi.TYPE_STRING, 
                                enum=['MIN', 'HOUR', 'DAY'], 
                                description="Unidad de tiempo para la duración de la reserva"
                            )
                        }
                    )
                )
            )
        }
    )

    def get(self, request, IDcommunity):
        common_areas = CommonArea.objects.filter(community_id=IDcommunity)
        serializer = CommonAreaSerializer(common_areas, many=True)
        return Response(serializer.data)

class CommonAreaDetailAPIView(APIView):
    def get(self, request, IDcommunity, area_id):
        common_area = get_object_or_404(CommonArea, community_id=IDcommunity, area_id=area_id)
        serializer = CommonAreaSerializer(common_area)
        return Response(serializer.data)

    def put(self, request, IDcommunity, area_id):
        common_area = get_object_or_404(CommonArea, community_id=IDcommunity, area_id=area_id)
        serializer = CommonAreaSerializer(common_area, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, IDcommunity, area_id):
        common_area = get_object_or_404(CommonArea, community_id=IDcommunity, area_id=area_id)
        common_area.delete()
        return Response({'message': 'Área común eliminada correctamente'}, status=status.HTTP_204_NO_CONTENT)

class ReservationListAPIView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()  # Esto asegura que la clase tiene un queryset por defecto

    @swagger_auto_schema(
        operation_description="Obtener una lista de reservas para un área común específica en una comunidad.",
        responses={
            200: openapi.Response(
                description="Lista de reservas obtenida exitosamente.",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'reservation_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID relativo de la reserva."),
                            'start_time': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fecha y hora de inicio de la reserva."),
                            'end_time': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fecha y hora de finalización de la reserva."),
                            'user': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID del usuario que creó la reserva."),
                            'neighbor': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID relativo del vecino para el que se hizo la reserva."),
                            'common_area': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID relativo del área común reservada."),
                            'community': openapi.Schema(type=openapi.TYPE_STRING, description="ID de la comunidad asociada."),
                            'duration': openapi.Schema(type=openapi.TYPE_INTEGER, description="Duración de la reserva."),
                            'time_unit': openapi.Schema(type=openapi.TYPE_STRING, description="Unidad de tiempo de la reserva."),
                        }
                    )
                )
            ),
            404: openapi.Response(description="No se encontraron reservas para la comunidad o área común especificada.")
        }
    )

    def get_queryset(self):
        IDcommunity = self.kwargs['IDcommunity']
        common_area_id = self.kwargs['common_area_id']
        return Reservation.objects.filter(community=IDcommunity, common_area=common_area_id)

class ReservationCreateAPIView(CreateAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    @swagger_auto_schema(
        operation_description="Crear una nueva reserva para un área común específica en una comunidad. Los campos 'community' y 'common_area' se obtienen desde la URL, y el 'user' es el que hace la solicitud.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['start_time', 'end_time', 'duration', 'time_unit'],
            properties={
                'start_time': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fecha y hora de inicio de la reserva (Formato ISO 8601)."),
                'end_time': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fecha y hora de finalización de la reserva (Formato ISO 8601)."),
                'neighbor': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID relativo del vecino para el que se hace la reserva (opcional)."),
                'duration': openapi.Schema(type=openapi.TYPE_INTEGER, description="Duración de la reserva en la unidad de tiempo especificada."),
                'time_unit': openapi.Schema(type=openapi.TYPE_STRING, enum=['MIN', 'HOUR', 'DAY'], description="Unidad de tiempo para la duración de la reserva.")
            }
        ),
        responses={
            201: openapi.Response(
                description="Reserva creada exitosamente.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'reservation_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID de la reserva creada."),
                        'start_time': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fecha y hora de inicio de la reserva."),
                        'end_time': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fecha y hora de finalización de la reserva."),
                        'user': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID del usuario que creó la reserva."),
                        'neighbor': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID relativo del vecino para el que se hizo la reserva."),
                        'common_area': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID relativo del área común reservada."),
                        'community': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID de la comunidad asociada."),
                        'duration': openapi.Schema(type=openapi.TYPE_INTEGER, description="Duración de la reserva."),
                        'time_unit': openapi.Schema(type=openapi.TYPE_STRING, description="Unidad de tiempo de la reserva.")
                    }
                )
            ),
            400: openapi.Response(description="Error al crear la reserva.")
        }
    )
    def perform_create(self, serializer):
        IDcommunity = self.kwargs['IDcommunity']
        common_area_id = self.kwargs['common_area_id']
        user = self.request.user
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']

        # Comprobar si ya existe una reserva en el mismo rango de tiempo
        if Reservation.objects.filter(
                community_id=IDcommunity,
                common_area_id=common_area_id,
                start_time__lt=end_time,
                end_time__gt=start_time
        ).exists():
            raise serializers.ValidationError("Ya existe una reserva en este intervalo de tiempo.")

        # Guardar la reserva si no hay conflictos
        serializer.save(
            community_id=IDcommunity,
            common_area_id=common_area_id,
            user=user
        )

class DeleteReservationAPIView(APIView):

    @swagger_auto_schema(
        operation_description="Eliminar una reserva específica para un área común en una comunidad.",
        responses={
            204: openapi.Response(description="Reserva eliminada exitosamente."),
            404: openapi.Response(description="No se encontró la reserva."),
        }
    )
    def delete(self, request, IDcommunity, common_area_id, reservation_id):
        # Obtener la comunidad, área común y la reserva correspondiente
        community = get_object_or_404(Community, community_id=IDcommunity)
        common_area = get_object_or_404(CommonArea, community=community, area_id=common_area_id)
        reservation = get_object_or_404(Reservation, community=community, common_area=common_area, reservation_id=reservation_id)

        # Eliminar la reserva
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)