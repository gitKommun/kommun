from rest_framework import serializers
from .models import Community, PersonCommunity, Role
from properties.models import Property
from common_areas.models import CommonArea

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'

class CommunityDetailSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()
    common_zones = serializers.SerializerMethodField()
    profiles = serializers.SerializerMethodField()
    province_name = serializers.CharField(source='province.name', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Community
        fields = '__all__'
        extra_fields = ['province_name', 'city_name']

    def get_properties(self, obj):
        return Property.objects.filter(community=obj).count()
    
    def get_common_zones(self, obj):
        return CommonArea.objects.filter(community=obj).count()
    
    def get_profiles(self, obj):
        return PersonCommunity.objects.filter(community=obj).count()
    
        

class PersonCommunitySerializer(serializers.ModelSerializer):
    roles = serializers.SlugRelatedField(
        many=True,
        slug_field='name',  # Devolver el nombre del rol en lugar del ID
        queryset=Role.objects.all()
    )
    class Meta:
        model = PersonCommunity
        exclude = ['id']
        read_only_fields = ['community', 'person_id', 'roles']
        
class PersonCommunityNeighborsSerializer(serializers.ModelSerializer):
    roles = serializers.SlugRelatedField(
        many=True,
        slug_field='name',  # Devolver el nombre del rol en lugar del ID
        queryset=Role.objects.all()
    )

    class Meta:
        model = PersonCommunity
        fields = ['person_id', 'name', 'surnames', 'roles']
