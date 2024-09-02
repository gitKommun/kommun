from rest_framework import serializers
from .models import Community, PersonCommunity, UserCommunityRole
from properties.models import Property
from common_areas.models import CommonArea

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'

class CommunityDetailSerializer(serializers.ModelSerializer):
    properties = serializers.SerializerMethodField()
    common_zones = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()
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
    
    def get_users(self, obj):
        return UserCommunityRole.objects.filter(community=obj).count()
    


class UserCommunityRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCommunityRole

        #fields = '__all__'
        fields = ['community','user']
        

class PersonCommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonCommunity
        fields = '__all__'
        read_only_fields = ['community', 'property_id']
        
class UserCommunityRoleSerializerTest(serializers.ModelSerializer):
    personal_data = serializers.SerializerMethodField()

    class Meta:
        model = UserCommunityRole
        fields = ['roles', 'user_status', 'personal_data']

    def get_personal_data(self, obj):
        # Check if there's an associated User and use their data if available
        if obj.user:
            return {
                'email': obj.user.email,
                'name': obj.user.name,
                'surnames': obj.user.surnames,
                'birthdate': obj.user.birthdate,
                'address': obj.user.address,
                'phone_number': obj.user.phone_number,
                'personal_id_number': obj.user.personal_id_number,
                'personal_id_type': obj.user.personal_id_type
            }
        # Otherwise, use the data from PersonCommunity
        elif obj.person:
            return {
                'email': obj.person.email,
                'name': obj.person.name,
                'surnames': obj.person.surnames,
                'birthdate': obj.person.birthdate,
                'address': obj.person.address,
                'phone_number': obj.person.phone_number,
                'personal_id_number': obj.person.personal_id_number,
                'personal_id_type': obj.person.personal_id_type
            }
        return {} 