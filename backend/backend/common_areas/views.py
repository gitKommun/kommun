from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import CommonArea, Reservation
from communities.models import Community

from .serializers import CommonAreaSerializer, ReservationSerializer


class CommonAreaCreateAPIView(APIView):
    def post(self, request, IDcommunity):
        data = request.data.copy()
        data['community'] = IDcommunity
        serializer = CommonAreaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class CommonAreaListCreateAPIView(APIView):
    def get(self, request, IDcommunity):
        common_areas = CommonArea.objects.filter(community_id=IDcommunity)
        serializer = CommonAreaSerializer(common_areas, many=True)
        return Response(serializer.data)

    def post(self, request, IDcommunity):
        community = get_object_or_404(Community, pk=IDcommunity)
        request.data['community'] = community.id

        serializer = CommonAreaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def get_queryset(self):
        IDcommunity = self.kwargs['IDcommunity']
        common_area_id = self.kwargs['common_area_id']
        return Reservation.objects.filter(community=IDcommunity, common_area=common_area_id)

class ReservationCreateAPIView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()  # Esto asegura que la clase tiene un queryset por defecto

    def perform_create(self, serializer):
        IDcommunity = self.kwargs['IDcommunity']
        common_area_id = self.kwargs['common_area_id']
        serializer.save(community_id=IDcommunity, common_area_id=common_area_id)


class ReservationDeleteAPIView(generics.DestroyAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        IDcommunity = self.kwargs['IDcommunity']
        common_area_id = self.kwargs['common_area_id']
        reservation_id = self.kwargs['reservation_id']
        return Reservation.objects.filter(community__id=IDcommunity, common_area_id=common_area_id, id=reservation_id)