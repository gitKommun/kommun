from rest_framework import serializers
from .models import Vote, Option, VoteRecord

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        exclude = ['created_by', 'community']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        exclude = ['vote']

class VoteRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteRecord
        exclude = ['vote', 'recorded_by']
