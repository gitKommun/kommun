from rest_framework import serializers
from .models import Claim, ClaimComment, ClaimStatusRecord

class ClaimStatusRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimStatusRecord
        fields = ['status', 'changed_by_full_name', 'timestamp']



class ClaimSerializer(serializers.ModelSerializer):
    status_records = ClaimStatusRecordSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, allow_null=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, allow_null=True)
    incident_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, allow_null=True)
    class Meta:
        model = Claim
        fields = [
            'claim_id', 'title', 'description', 'category', 'priority', 'status',
            'incident_date', 'problem_persists', 'created_at', 'updated_at', 'status_records'
        ]
        read_only_fields = ['claim_id' ]



class ClaimCommentSerializer(serializers.ModelSerializer):
    user_fullname = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = ClaimComment
        fields = [ 'claim_comment_id',  'comment', 'created_at', 'user_fullname']
        read_only_fields = ['user_fullname','created_at','claim_comment_id']
    
    def get_user_fullname(self, obj):
        return f"{obj.user.name} {obj.user.surnames}".strip() if obj.user else None


class ClaimDetailSerializer(serializers.ModelSerializer):
    comments = ClaimCommentSerializer(many=True, read_only=True)
    status_records = ClaimStatusRecordSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    incident_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, allow_null=True)
    user_fullname = serializers.SerializerMethodField()

    class Meta:
        model = Claim
        fields = [
            'claim_id', 'title', 'description', 'category', 'priority', 'status',
            'incident_date', 'problem_persists', 'created_at', 'updated_at', 
            'comments', 'status_records', 'user_fullname'
        ]
        read_only_fields = ['claim_id', 'status', 'created_at', 'updated_at', 'comments', 'status_records','user_fullname']
    
    def get_user_fullname(self, obj):
        return f"{obj.user.name} {obj.user.surnames}".strip() if obj.user else None
