from rest_framework import serializers
from .models import CommonArea, Reservation

class CommonAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonArea
        fields = '__all__'
        
class ReservationSerializer(serializers.ModelSerializer):
    reservation_id = serializers.IntegerField(read_only=True)  # Solo lectura ya que se autogenera

    class Meta:
        model = Reservation
        fields = [
            'reservation_id',  # Añadido para incluirlo en la respuesta
            'community',
            'common_area',
            'user',
            'neighbor',
            'start_time',
            'end_time',
            'duration',
            'time_unit'
        ]
        read_only_fields = ['reservation_id','community', 'common_area', 'user']  # Estos campos se llenan automáticamente