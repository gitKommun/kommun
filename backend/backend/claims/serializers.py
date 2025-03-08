from rest_framework import serializers
from .models import Claim, ClaimComment, ClaimStatusRecord

class ClaimStatusRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimStatusRecord
        fields = ['status', 'changed_by_full_name', 'timestamp']



class ClaimSerializer(serializers.ModelSerializer):
    status_records = ClaimStatusRecordSerializer(many=True, read_only=True)
    class Meta:
        model = Claim
        fields = [
            'claim_id', 'title', 'description', 'category', 'priority', 'status',
            'incident_date', 'problem_persists', 'created_at', 'updated_at', 'status_records'
        ]
        read_only_fields = ['claim_id' ]



class ClaimCommentSerializer(serializers.ModelSerializer):
    user_fullname = serializers.SerializerMethodField()
    class Meta:
        model = ClaimComment
        fields = [ 'claim_comment_id',  'comment', 'created_at', 'user_fullname']
        read_only_fields = ['user_fullname','created_at','claim_comment_id']
    
    def get_user_fullname(self, obj):
        return f"{obj.user.name} {obj.user.surnames}".strip() if obj.user else None


class ClaimDetailSerializer(serializers.ModelSerializer):
    comments = ClaimCommentSerializer(many=True, read_only=True)
    status_records = ClaimStatusRecordSerializer(many=True, read_only=True)
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

class ClaimTimelineSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=['status_change', 'message'])
    timestamp = serializers.DateTimeField()
    data = serializers.DictField()

class ClaimDetailTimeLineSerializer(serializers.ModelSerializer):
    comments = ClaimCommentSerializer(many=True, read_only=True)
    timeline = serializers.SerializerMethodField()  # Timeline en vez de status_records
    user_fullname = serializers.SerializerMethodField()

    class Meta:
        model = Claim
        fields = [
            'claim_id', 'title', 'description', 'category', 'priority', 'status',
            'incident_date', 'problem_persists', 'created_at', 'updated_at', 
            'comments', 'timeline', 'user_fullname'
        ]
        read_only_fields = ['claim_id', 'status', 'created_at', 'updated_at', 'comments', 'timeline', 'user_fullname']

    def get_user_fullname(self, obj):
        return f"{obj.user.name} {obj.user.surnames}".strip() if obj.user else None

    def get_timeline(self, obj):
        timeline_entries = []

        # 🔹 Obtener cambios de estado
        status_changes = obj.status_records.all()
        for i in range(len(status_changes)):
            previous_status = status_changes[i - 1].status if i > 0 else None
            timeline_entries.append({
                "type": "status_change",
                "timestamp": status_changes[i].timestamp,
                "data": {
                    "previous_status": previous_status,
                    "new_status": status_changes[i].status
                }
            })

        # 🔹 Obtener mensajes de la incidencia
        messages = obj.messages.all()
        for message in messages:
            timeline_entries.append({
                "type": "message",
                "timestamp": message.created_at,
                "data": {
                    "message_id": message.message_id,
                    "message_type": message.message_type,
                    "message": message.message,
                    "user_fullname": f"{message.user.name} {message.user.surnames}".strip() if message.user else None
                }
            })

        # 📌 Ordenar de más reciente a más antiguo
        timeline_entries.sort(key=lambda x: x["timestamp"], reverse=True)

        return timeline_entries