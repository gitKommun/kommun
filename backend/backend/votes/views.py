from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import VoteSerializer, OptionSerializer
from communities.models import Community, PersonCommunity
from .models import Vote, Option, VoteRecord


class CreateVoteAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Crear una votación y asignar votantes elegibles mediante el ID relativo de la comunidad.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="Título de la votación"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="Descripción de la votación"),
                'start_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fecha de inicio"),
                'end_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fecha de finalización"),
                'vote_type': openapi.Schema(type=openapi.TYPE_STRING, enum=['simple', 'multiple_choice'], description="Tipo de votación"),
                'eligible_voters': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description="Lista de person_id relativos (vecinos que pueden votar)"
                ),
                'options': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description="Lista de opciones de votación"
                )
            }
        ),
        responses={201: "Votación creada exitosamente.", 400: "Datos inválidos."}
    )
    def post(self, request, IDcommunity):
        # Obtener la comunidad
        community = get_object_or_404(Community, community_id=IDcommunity)

        # Extraer los datos de la solicitud
        title = request.data.get('title')
        description = request.data.get('description')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        vote_type = request.data.get('vote_type')
        eligible_voters_ids = request.data.get('eligible_voters', [])
        options_data = request.data.get('options', [])

        # Crear el objeto Vote
        vote = Vote.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            vote_type=vote_type,
            created_by=request.user,
            community=community
        )

        # Asignar los votantes elegibles usando person_id relativo dentro de la comunidad
        valid_voters = []
        for person_id in eligible_voters_ids:
            try:
                voter = PersonCommunity.objects.get(community=community, person_id=person_id)
                valid_voters.append(voter)
            except PersonCommunity.DoesNotExist:
                return Response({'error': f'El vecino con person_id {person_id} no existe en esta comunidad.'}, status=status.HTTP_400_BAD_REQUEST)

        # Asignar los votantes válidos a la votación
        if valid_voters:
            vote.eligible_voters.set(valid_voters)
        else:
            return Response({'error': 'No se encontraron votantes elegibles válidos.'}, status=status.HTTP_400_BAD_REQUEST)

        # Crear las opciones de la votación
        for option_text in options_data:
            Option.objects.create(vote=vote, option_text=option_text)

        return Response({"message": "Votación creada exitosamente", "vote_id": vote.vote_id}, status=status.HTTP_201_CREATED)

class CastVoteAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Registrar un voto para una votación específica.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['person_id', 'option_ids'],
            properties={
                'person_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID relativo del vecino en la comunidad"),
                'option_ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description="Lista de IDs relativos de las opciones seleccionadas"
                ),
                'delegated_to': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID del vecino al que se delega el voto, opcional")
            },
        ),
        responses={
            201: openapi.Response(description="Voto registrado con éxito."),
            400: openapi.Response(description="Error al registrar el voto.")
        },
        manual_parameters=[
            openapi.Parameter('IDcommunity', openapi.IN_PATH, description="ID de la comunidad", type=openapi.TYPE_STRING),
            openapi.Parameter('vote_id', openapi.IN_PATH, description="ID de la votación dentro de la comunidad", type=openapi.TYPE_INTEGER),
        ]
    )

    def post(self, request, IDcommunity, vote_id):
        # Obtener el voto y la comunidad
        community = get_object_or_404(Community, community_id=IDcommunity)
        vote = get_object_or_404(Vote, community=community, vote_id=vote_id)

        # Obtener el perfil del vecino (PersonCommunity) del usuario
        person_community = get_object_or_404(PersonCommunity, user=request.user, community=community)

        # Verificar si el usuario es elegible para votar
        if person_community not in vote.eligible_voters.all():
            raise PermissionDenied("No tienes permiso para votar en esta votación.")

        # Verificar si el usuario ya ha votado
        if VoteRecord.objects.filter(vote=vote, neighbor=person_community).exists():
            return Response({'error': 'Ya has votado en esta votación.'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener las opciones seleccionadas
        option_ids = request.data.get('option_ids', [])
        if not isinstance(option_ids, list) or len(option_ids) == 0:
            return Response({'error': 'Debes seleccionar al menos una opción.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validar el tipo de votación
        if vote.vote_type == Vote.VoteType.SIMPLE and len(option_ids) > 1:
            return Response({'error': 'Esta votación permite seleccionar solo una opción.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar que las opciones seleccionadas sean válidas usando option_id
        valid_option_ids = list(vote.options.values_list('option_id', flat=True))  # Obtener los option_ids válidos para la votación
        if not all(option_id in valid_option_ids for option_id in option_ids):
            return Response({'error': 'Una o más opciones seleccionadas no son válidas.'}, status=status.HTTP_400_BAD_REQUEST)

        # Crear el registro de votación
        vote_record = VoteRecord.objects.create(
            vote=vote,
            neighbor=person_community,
            recorded_by=request.user
        )
        # Relacionar las opciones seleccionadas al registro de votos
        vote_record.options.add(*Option.objects.filter(vote=vote, option_id__in=option_ids))

        return Response({'message': 'Voto registrado correctamente.'}, status=status.HTTP_201_CREATED)


class CommunityVotesListAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Obtiene el listado de todas las votaciones de una comunidad, con un resumen de votos por cada opción y el estado de la votación.",
        responses={
            200: openapi.Response(
                description="Lista de votaciones de la comunidad",
                examples={
                    "application/json": [
                        {
                            "vote_id": 1,
                            "title": "Presupuesto 2023",
                            "description": "Aprobación del presupuesto",
                            "start_date": "2023-10-01T10:00:00Z",
                            "end_date": "2023-10-31T23:59:00Z",
                            "status": "open",
                            "options": [
                                {"option_id": 1, "option_text": "A favor", "vote_count": 30},
                                {"option_id": 2, "option_text": "En contra", "vote_count": 10}
                            ],
                            "pending_votes": 15
                        },
                        {
                            "vote_id": 2,
                            "title": "Renovación de la piscina",
                            "description": "Renovación de las instalaciones de la piscina",
                            "start_date": "2023-09-01T10:00:00Z",
                            "end_date": "2023-09-30T23:59:00Z",
                            "status": "closed",
                            "options": [
                                {"option_id": 1, "option_text": "A favor", "vote_count": 45},
                                {"option_id": 2, "option_text": "En contra", "vote_count": 5}
                            ],
                            "pending_votes": 0
                        }
                    ]
                }
            ),
            404: "Comunidad no encontrada"
        }
    )
    def get(self, request, IDcommunity):
        # Filtrar votaciones por comunidad
        votes = Vote.objects.filter(community__community_id=IDcommunity)

        # Lista para almacenar la información de cada votación
        votes_data = []
        current_time = timezone.now()


        for vote in votes:
            # Determinar el estado de la votación
            if vote.start_date > current_time:
                vote_status = "not_started"
            elif vote.end_date < current_time or vote.eligible_voters.count() == vote.vote_records.count():
                vote_status = "closed"
            else:
                vote_status = "open"

            # Resumen de votos por cada opción
            options_summary = []
            for option in vote.options.all():
                vote_count = VoteRecord.objects.filter(vote=vote, options=option).count()
                options_summary.append({
                    "option_id": option.option_id,
                    "option_text": option.option_text,
                    "vote_count": vote_count
                })

            # Calcular votos pendientes
            pending_votes = vote.eligible_voters.count() - vote.vote_records.count()

            # Agregar datos de la votación al resultado final
            votes_data.append({
                "vote_id": vote.vote_id,
                "title": vote.title,
                "description": vote.description,
                "start_date": vote.start_date,
                "end_date": vote.end_date,
                "status": vote_status,
                "options": options_summary,
                "pending_votes": pending_votes
            })

        return Response(votes_data, status=status.HTTP_200_OK)

class VoteDetailAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Obtener los detalles y resultados de una votación específica.",
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'vote_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID de la votación relativa a la comunidad"),
                    'title': openapi.Schema(type=openapi.TYPE_STRING, description="Título de la votación"),
                    'description': openapi.Schema(type=openapi.TYPE_STRING, description="Descripción de la votación"),
                    'start_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fecha de inicio de la votación"),
                    'end_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fecha de finalización de la votación"),
                    'vote_type': openapi.Schema(type=openapi.TYPE_STRING, description="Tipo de votación"),
                    'results': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'option_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID relativo de la opción"),
                                'option_text': openapi.Schema(type=openapi.TYPE_STRING, description="Texto de la opción"),
                                'vote_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="Número de votos recibidos")
                            }
                        ),
                        description="Lista de resultados de la votación"
                    ),
                    'pending_votes': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'total': openapi.Schema(type=openapi.TYPE_INTEGER, description="Número total de votos pendientes"),
                            'details': openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Schema(
                                    type=openapi.TYPE_OBJECT,
                                    properties={
                                        'neighbor_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID relativo del vecino en la comunidad"),
                                        'neighbor_name': openapi.Schema(type=openapi.TYPE_STRING, description="Nombre del vecino"),
                                        'delegated_to_name': openapi.Schema(type=openapi.TYPE_STRING, description="Nombre del delegado, si lo hay")
                                    }
                                ),
                                description="Lista de vecinos con votos pendientes"
                            )
                        }
                    ),
                    'votes_received': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'neighbor_name': openapi.Schema(type=openapi.TYPE_STRING, description="Nombre del votante"),
                                'delegated_to_name': openapi.Schema(type=openapi.TYPE_STRING, description="Nombre del delegado (si aplica)"),
                                'options_selected': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
                                'timestamp': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fecha de registro del voto")
                            }
                        ),
                        description="Detalles de los votos recibidos"
                    )
                }
            ),
            404: "Votación no encontrada."
        }
    )
    def get(self, request, IDcommunity, vote_id):
        # Obtener la comunidad y la votación
        community = get_object_or_404(Community, community_id=IDcommunity)
        vote = get_object_or_404(Vote, community=community, vote_id=vote_id)

        # Obtener los resultados como lista
        results = [
            {
                'option_id': option.option_id,
                'option_text': option.option_text,
                'vote_count': option.vote_records_multiple.count()
            }
            for option in vote.options.all()
        ]

        # Votos pendientes
        total_eligible_voters = vote.eligible_voters.count()
        votes_received_count = vote.vote_records.count()
        pending_votes_count = total_eligible_voters - votes_received_count

        # Obtener detalles de votos pendientes
        voted_neighbors = vote.vote_records.values_list('neighbor_id', flat=True)
        pending_voters = vote.eligible_voters.exclude(id__in=voted_neighbors)
        
        pending_votes_details = [
            {
                'neighbor_id': neighbor.person_id,
                'neighbor_name': f"{neighbor.name} {neighbor.surnames}",
                'delegated_to_name': None  # Puedes ajustar si necesitas información específica sobre el delegado
            }
            for neighbor in pending_voters
        ]

        # Detalle de votos recibidos
        votes_received_details = [
            {
                'neighbor_name': f"{record.neighbor.name} {record.neighbor.surnames}",
                'delegated_to_name': f"{record.delegated_to.name} {record.delegated_to.surnames}" if record.delegated_to else None,
                'options_selected': [opt.option_text for opt in record.options.all()],
                'timestamp': record.timestamp
            }
            for record in vote.vote_records.select_related('neighbor', 'delegated_to').prefetch_related('options')
        ]

        # Respuesta con la información de la votación y los resultados
        response_data = {
            'vote_id': vote.vote_id,
            'title': vote.title,
            'description': vote.description,
            'start_date': vote.start_date,
            'end_date': vote.end_date,
            'vote_type': vote.vote_type,
            'results': results,
            'pending_votes': {
                'total': pending_votes_count,
                'details': pending_votes_details
            },
            'votes_received': votes_received_details
        }

        return Response(response_data, status=status.HTTP_200_OK)

class UpdateVoteAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Actualizar una votación específica.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['title', 'start_date', 'end_date', 'vote_type'],  
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="Título de la votación"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="Descripción de la votación"),
                'start_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fecha de inicio de la votación"),
                'end_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description="Fecha de finalización de la votación"),
                'vote_type': openapi.Schema(type=openapi.TYPE_STRING, enum=['simple', 'multiple_choice'], description="Tipo de votación"),
                'options': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description="Lista de opciones de la votación (como strings)"
                ),
            }
        ),
        responses={
            200: openapi.Response(description="Votación actualizada con éxito."),
            400: openapi.Response(description="Error al actualizar la votación.")
        }
    )
    def put(self, request, IDcommunity, vote_id):
        # Obtener la comunidad y la votación
        community = get_object_or_404(Community, community_id=IDcommunity)
        vote = get_object_or_404(Vote, community=community, vote_id=vote_id)

        # Serializar los datos de la votación
        serializer = VoteSerializer(vote, data=request.data, partial=True)
        if serializer.is_valid():
            updated_vote = serializer.save()

            # Actualizar las opciones si se proporcionan
            options_data = request.data.get('options', [])
            existing_options = {opt.option_id: opt for opt in Option.objects.filter(vote=updated_vote)}

            # Actualizar opciones existentes o crear nuevas si es necesario
            new_option_id = max(existing_options.keys(), default=0) + 1
            updated_option_ids = []

            for index, option_text in enumerate(options_data, start=1):
                if index in existing_options:
                    # Actualizar el texto de las opciones existentes
                    existing_option = existing_options[index]
                    if existing_option.option_text != option_text:
                        existing_option.option_text = option_text
                        existing_option.save()
                    updated_option_ids.append(existing_option.option_id)
                else:
                    # Crear nuevas opciones si no existen
                    Option.objects.create(vote=updated_vote, option_id=new_option_id, option_text=option_text)
                    updated_option_ids.append(new_option_id)
                    new_option_id += 1

            # Eliminar las opciones que no están en la lista actualizada
            for option_id, option in existing_options.items():
                if option_id not in updated_option_ids:
                    option.delete()

            return Response(VoteSerializer(updated_vote).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteVoteAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Eliminar una votación específica.",
        responses={
            204: openapi.Response(description="Votación eliminada con éxito."),
            404: openapi.Response(description="Votación no encontrada.")
        }
    )
    def delete(self, request, IDcommunity, vote_id):
        # Obtener la comunidad y la votación
        community = get_object_or_404(Community, community_id=IDcommunity)
        vote = get_object_or_404(Vote, community=community, vote_id=vote_id)

        # Eliminar la votación
        vote.delete()
        return Response({'message': 'Votación eliminada con éxito.'}, status=status.HTTP_204_NO_CONTENT)