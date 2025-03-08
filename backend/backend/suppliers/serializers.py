from rest_framework import serializers
from .models import Supplier, WorkOrder, WorkOrderSupplierRequest
from django.utils import timezone

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"

class WorkOrderCreateSerializer(serializers.ModelSerializer):
    supplier_request_id = serializers.UUIDField(read_only=True)  # Campo solo para la respuesta

    class Meta:
        model = WorkOrder
        fields = ['title', 'description', 'supplier', 'start_date', 'work_order_id', 'order_number', 'status', 'supplier_request_id']
        read_only_fields = ['work_order_id', 'order_number', 'status', 'supplier_request_id']
        
    def validate_start_date(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("La fecha de inicio no puede ser en el pasado")
        return value

class WorkOrderSupplierResponseSerializer(serializers.ModelSerializer):
    start_date = serializers.DateTimeField(required=False, write_only=True)

    class Meta:
        model = WorkOrderSupplierRequest
        fields = ['status', 'rejection_reason', 'start_date']
        extra_kwargs = {
            'rejection_reason': {'required': False},
        }

    def validate(self, data):
        if data.get('status') == 'accepted' and not data.get('start_date'):
            raise serializers.ValidationError(
                {"start_date": "Debe proporcionar una fecha de inicio para el trabajo"}
            )
        return data
