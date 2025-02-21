
from django.shortcuts import get_object_or_404
from django.utils.timezone import make_aware, is_naive
from datetime import datetime, timedelta
from django.db import transaction

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import CommonArea, Reservation
from communities.models import Community, PersonCommunity
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



class CommonAreaAvailableSlotsAPIView(APIView):
    @swagger_auto_schema(
        operation_description=(
            "Obtiene los slots disponibles en un área común para una fecha específica. \n\n"
            "- Se debe pasar el parámetro `date` en formato `YYYY-MM-DD` en la URL.\n"
            "- Si el área común no es reservable, devolverá un error.\n"
            "- Se devuelve una lista de slots indicando si están reservados (`reserved: true/false`).\n"
            "- Si el slot está reservado, se incluirá `reservation_id` y los datos del `neighbor` (persona que usará la reserva). \n\n"
            "**Ejemplo de solicitud:**\n"
            "```http\n"
            "GET /common_areas/{IDcommunity}/{area_id}/available_slots/?date=2025-02-20\n"
            "```"
        ),
        manual_parameters=[
            openapi.Parameter('IDcommunity', openapi.IN_PATH, description="ID de la comunidad", type=openapi.TYPE_STRING),
            openapi.Parameter('area_id', openapi.IN_PATH, description="ID del área común relativo a la comunidad", type=openapi.TYPE_INTEGER),
            openapi.Parameter('date', openapi.IN_QUERY, description="Fecha en formato YYYY-MM-DD", type=openapi.TYPE_STRING, required=True),
        ],
        responses={
            200: openapi.Response(
                description="Lista de slots disponibles y ocupados para el área en la fecha especificada.",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'slot_start': openapi.Schema(type=openapi.TYPE_STRING, description="Hora de inicio del slot"),
                            'slot_end': openapi.Schema(type=openapi.TYPE_STRING, description="Hora de fin del slot"),
                            'reserved': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Indica si el slot está reservado"),
                            'reservation_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID de la reserva", nullable=True),
                            'neighbor': openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'person_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID del vecino para quien se hizo la reserva"),
                                    'fullName': openapi.Schema(type=openapi.TYPE_STRING, description="Nombre completo del vecino que usará la reserva")
                                },
                                description="Vecino que usará la reserva (null si no está reservado)",
                                nullable=True
                            )
                        }
                    )
                )
            ),
            400: openapi.Response(description="Error en los parámetros de entrada."),
            404: openapi.Response(description="Área común no encontrada o no reservable."),
        }
    )
    def get(self, request, IDcommunity, area_id):
        # Verificar si se proporcionó la fecha
        date_str = request.GET.get('date')
        if not date_str:
            return Response({'error': 'Se requiere un parámetro `date` en formato YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener el área común
        common_area = CommonArea.objects.filter(community__community_id=IDcommunity, area_id=area_id).first()
        if not common_area:
            return Response({'error': 'Área común no encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        
        if not common_area.reservable:
            return Response({'error': 'Esta área común no es reservable.'}, status=status.HTTP_400_BAD_REQUEST)

        if not common_area.reservation_duration or not common_area.time_unit:
            return Response({'error': 'El área común no tiene configurada la duración de reserva.'}, status=status.HTTP_400_BAD_REQUEST)

        # Convertir la unidad de tiempo en minutos
        time_unit_map = {'MIN': 1, 'HOUR': 60, 'DAY': 1440}
        slot_duration_minutes = common_area.reservation_duration * time_unit_map[common_area.time_unit] 

        if common_area.time_unit == 'DAY':
            # Si la unidad de tiempo es 'DÍA', se considera que la duracion es la diferencia en minutos entre el usage_start y el usage_end
            usage_start_time = datetime.combine(datetime.min, common_area.usage_start)
            usage_end_time = datetime.combine(datetime.min, common_area.usage_end)
            slot_duration_minutes = (usage_end_time - usage_start_time).seconds // 60

        print(f"{common_area.time_unit} Duración del slot: {slot_duration_minutes} minutos")

        # Definir la franja horaria de la zona común
        if not common_area.usage_start or not common_area.usage_end:
            return Response({'error': 'El área común no tiene configurados los horarios de uso.'}, status=status.HTTP_400_BAD_REQUEST)

        usage_start = make_aware(datetime.combine(selected_date, common_area.usage_start))
        usage_end = make_aware(datetime.combine(selected_date, common_area.usage_end))
        if common_area.usage_end == datetime.min.time():
            usage_end += timedelta(days=1)

        # Obtener reservas existentes para ese día
        existing_reservations = Reservation.objects.filter(
            common_area=common_area,
            start_time__date=selected_date
        ).order_by('start_time')

        # Generar los slots según la configuración
        available_slots = []
        current_time = usage_start


        while current_time + timedelta(minutes=slot_duration_minutes) <= usage_end:
            slot_end = current_time + timedelta(minutes=slot_duration_minutes)

            # Verificar si este slot está reservado
            reserved = None
            for reservation in existing_reservations:
                if reservation.start_time < slot_end and reservation.end_time > current_time:
                    reserved = reservation
                    break

            if reserved:
                available_slots.append({
                    'slot_start': current_time.strftime("%H:%M"),
                    'slot_end': slot_end.strftime("%H:%M"),
                    'reserved': True,
                    'reservation_id': reserved.reservation_id,
                    'neighbor': {
                        'person_id': reserved.neighbor.person_id if reserved.neighbor else None,
                        'fullName': f"{reserved.neighbor.name} {reserved.neighbor.surnames}" if reserved.neighbor else None
                    } if reserved.neighbor else None
                })
            else:
                available_slots.append({
                    'slot_start': current_time.strftime("%H:%M"),
                    'slot_end': slot_end.strftime("%H:%M"),
                    'reserved': False,
                    'reservation_id': None,
                    'neighbor': None
                })

            current_time += timedelta(minutes=slot_duration_minutes)

        return Response(available_slots, status=status.HTTP_200_OK)

class ReservationCreateAPIView(CreateAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()

    @swagger_auto_schema(
        operation_description="""
        Crea una nueva reserva en un área común específica dentro de una comunidad.
        
        📌 **Notas:**
        - La `community` y el `common_area` se determinan a partir de la URL.
        - El `user` es el usuario autenticado que realiza la solicitud.
        - Se debe proporcionar la `start_time` y `end_time` en formato ISO 8601.
        - Si `neighbor` no se envía, se asume que la reserva es para el usuario autenticado.
        - **Verificación de disponibilidad:** No se permiten reservas solapadas en el mismo intervalo de tiempo.
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['start_time', 'end_time'],
            properties={
                'start_time': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    format=openapi.FORMAT_DATETIME, 
                    description="Fecha y hora de inicio de la reserva (Formato ISO 8601, UTC)."
                ),
                'end_time': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    format=openapi.FORMAT_DATETIME, 
                    description="Fecha y hora de finalización de la reserva (Formato ISO 8601, UTC)."
                ),
                'neighbor': openapi.Schema(
                    type=openapi.TYPE_INTEGER, 
                    description="ID relativo del vecino (`person_id`) para quien se realiza la reserva (opcional)."
                )
            }
        ),
        responses={
            201: openapi.Response(
                description="Reserva creada con éxito.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'reservation_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID relativo de la reserva."),
                        'start_time': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Inicio de la reserva."),
                        'end_time': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fin de la reserva."),
                        'common_area': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID relativo del área común reservada."),
                        'neighbor': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID relativo del vecino para quien se hizo la reserva."),
                    }
                )
            ),
            400: openapi.Response(
                description="Error al crear la reserva. Puede deberse a que la zona no es reservable, la fecha no tiene el formato correcto o hay un conflicto de horarios."
            ),
            404: openapi.Response(description="Comunidad o área común no encontrada."),
            403: openapi.Response(description="No tienes permiso para reservar en esta área."),
        }
    )

    def perform_create(self, serializer):
        IDcommunity = self.kwargs['IDcommunity']
        common_area_id = self.kwargs['common_area_id']
        user = self.request.user

        #  Obtener la comunidad
        community = get_object_or_404(Community, community_id=IDcommunity)

        #  Obtener el área común por `area_id`
        common_area = get_object_or_404(CommonArea, community=community, area_id=common_area_id)

        #  Verificar que el área es reservable
        if not common_area.reservable:
            raise serializers.ValidationError("📌 Esta área común no es reservable.")

        #  Obtener datos de la solicitud
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']

        #  Convertir a timezone-aware solo si son naive
        if is_naive(start_time):
            start_time = make_aware(start_time)
        if is_naive(end_time):
            end_time = make_aware(end_time)

        #  Obtener el `neighbor` desde `person_id`
        person_id = self.request.data.get('neighbor', None)
        neighbor_instance = None
        if person_id:
            neighbor_instance = PersonCommunity.objects.filter(community=community, person_id=person_id).first()
            if not neighbor_instance:
                raise serializers.ValidationError("📌 El `person_id` proporcionado no pertenece a esta comunidad.")

        #  Verificar conflictos de horarios
        if Reservation.objects.filter(
            common_area=common_area,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists():
            raise serializers.ValidationError("📌 Ya existe una reserva en este intervalo de tiempo.")

        #  Asignar el ID relativo de la reserva
        with transaction.atomic():
            last_reservation = Reservation.objects.filter(
                community=community,
                common_area=common_area
            ).select_for_update().order_by('reservation_id').last()

            reservation_id = (last_reservation.reservation_id + 1) if last_reservation else 1

            #  Guardar la reserva con la instancia correcta de `neighbor`
            serializer.save(
                community=community,
                common_area=common_area,
                user=user,
                neighbor=neighbor_instance,  #  Pasamos la instancia correcta
                reservation_id=reservation_id
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