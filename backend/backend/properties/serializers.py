from rest_framework import serializers
from .models import Property, PropertyRelationship
from communities.serializers import PersonCommunitySerializer

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        #fields = '__all__'
        exclude = ['id']
        read_only_fields = ['community', 'property_id']


class PropertyOwnerSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ['property_id', 'address_complete', 'surface_area', 'participation_coefficient', 'usage', 'owner']

    def get_owner(self, obj):
        owner_relationship = obj.relationships.filter(type='owner').first()
        if owner_relationship and owner_relationship.person:
            return PersonCommunitySerializer(owner_relationship.person).data
        return None


class PropertyRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyRelationship
        fields = '__all__'

class PropertyRelationshipPersonSerializer(serializers.ModelSerializer):
    person_id = serializers.IntegerField(source='person.person_id', read_only=True)  # ID relativo de la persona en la comunidad
    name = serializers.CharField(source='person.name', read_only=True)
    surnames = serializers.CharField(source='person.surnames', read_only=True)

    class Meta:
        model = PropertyRelationship
        fields = ['type', 'person_id', 'name', 'surnames']
            

# Serializer for Property including the relationships
class PropertyDetailSerializer(serializers.ModelSerializer):
    relationships = PropertyRelationshipPersonSerializer(many=True)

    class Meta:
        model = Property
        fields = ['property_id', 'surface_area', 'participation_coefficient', 'usage', 'address_complete', 'block', 'staircase', 'floor', 'door', 'relationships']