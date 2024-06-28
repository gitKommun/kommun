from rest_framework import serializers
from .models import CommonArea, Reservation

class CommonAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommonArea
        fields = '__all__'
        #extra_kwargs = {'area_id': {'write_only': True}}

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'
