from rest_framework import serializers
from .models import Community, Property, UserCommunityRole

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['community','numberProperty', 'typeProperty', 'communityPropertyPercentage']
        extra_kwargs = {'community': {'write_only': True}}

class UserCommunityRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCommunityRole
        fields = '__all__'
        #fields = ['community','user', 'role']