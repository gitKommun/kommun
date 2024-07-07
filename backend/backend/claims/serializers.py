from rest_framework import serializers
from .models import Claim, ClaimComment, ClaimStatusRecord

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = [
            'title', 'description', 'category', 'priority', 'status',
            'incident_date', 'problem_persists', 
        ]
        read_only_fields = ['status']


class ClaimCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimComment
        fields = [ 'user', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']

class ClaimStatusRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimStatusRecord
        fields = ['id', 'claim', 'status', 'changed_by', 'timestamp']
        read_only_fields = ['id', 'changed_by', 'timestamp']

class ClaimDetailSerializer(serializers.ModelSerializer):
    comments = ClaimCommentSerializer(many=True, read_only=True)
    status_records = ClaimStatusRecordSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)

    class Meta:
        model = Claim
        fields = [
            'id', 'title', 'description', 'category', 'priority', 'status',
            'incident_date', 'problem_persists', 'created_at', 'updated_at', 
            'comments', 'status_records', 'user_name'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at', 'comments', 'status_records']
