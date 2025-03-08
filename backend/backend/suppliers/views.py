from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Supplier, WorkOrder, WorkOrderSupplierRequest
from .serializers import SupplierSerializer, WorkOrderCreateSerializer, WorkOrderSupplierResponseSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from claims.models import Claim, ClaimMessage
from communities.models import Community
from members.views import create_notification
from members.models import User, Notification

# 📌 Vista para LISTAR proveedores
class SupplierListAPIView(generics.ListAPIView):
    """
    supplier_list

    Obtiene el listado de proveedores con opción de filtrar por diferentes criterios.

    **Filtros disponibles:**
    - `company_name` → Filtra por nombre de empresa (búsqueda parcial).
    - `cif_nif` → Filtra por CIF/NIF exacto.
    - `type` → Filtra por el tipo de proveedor (ejemplo: electricidad, limpieza, etc.).
    - `rating` → Filtra por calificación mínima (ejemplo: `4` para proveedores con rating 4 o más).

    **Ejemplo de consulta:**  
    `/suppliers/?company_name=Lock&type=electricidad&rating=4`
    """

    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()

    @swagger_auto_schema(
        operation_description="Obtiene el listado de proveedores con opción de filtrar por nombre, CIF/NIF, tipo o rating.",
        manual_parameters=[
            openapi.Parameter("company_name", openapi.IN_QUERY, description="Filtra por nombre de empresa (parcial)", type=openapi.TYPE_STRING),
            openapi.Parameter("cif_nif", openapi.IN_QUERY, description="Filtra por CIF/NIF exacto", type=openapi.TYPE_STRING),
            openapi.Parameter("type", openapi.IN_QUERY, description="Filtra por tipo de proveedor (ejemplo: electricidad, limpieza, etc.)", type=openapi.TYPE_STRING),
            openapi.Parameter("rating", openapi.IN_QUERY, description="Filtra por calificación mínima (ejemplo: 4 para proveedores con rating 4 o más)", type=openapi.TYPE_INTEGER),
        ],
        responses={200: SupplierSerializer(many=True)}
    )
    def get_queryset(self):
        """
        Filtra los proveedores según los parámetros de búsqueda enviados en la URL.
        """
        queryset = Supplier.objects.all()
        company_name = self.request.query_params.get('company_name', None)
        cif_nif = self.request.query_params.get('cif_nif', None)
        provider_type = self.request.query_params.get('type', None)
        rating = self.request.query_params.get('rating', None)

        if company_name:
            queryset = queryset.filter(company_name__icontains=company_name)
        if cif_nif:
            queryset = queryset.filter(cif_nif=cif_nif)
        if provider_type:
            queryset = queryset.filter(type=provider_type)
        if rating:
            try:
                rating = int(rating)
                queryset = queryset.filter(rating__gte=rating)
            except ValueError:
                pass  # Ignora si el rating no es un número válido

        return queryset

# 📌 Vista para CREAR un proveedor
class SupplierCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Create a new supplier.",
        request_body=SupplierSerializer,
        responses={201: SupplierSerializer(), 400: "Invalid data"}
    )
    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 📌 Vista para OBTENER un proveedor por ID
class SupplierRetrieveAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a specific supplier by ID.",
        responses={200: SupplierSerializer(), 404: "Supplier not found"}
    )
    def get(self, request, supplier_id):
        supplier = generics.get_object_or_404(Supplier, supplier_id=supplier_id)
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 📌 Vista para ACTUALIZAR un proveedor
class SupplierUpdateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Update a supplier by ID.",
        request_body=SupplierSerializer,
        responses={200: SupplierSerializer(), 400: "Invalid data", 404: "Supplier not found"}
    )
    def put(self, request, supplier_id):
        supplier = generics.get_object_or_404(Supplier, supplier_id=supplier_id)
        serializer = SupplierSerializer(supplier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 📌 Vista para ELIMINAR un proveedor
class SupplierDeleteAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Delete a supplier by ID.",
        responses={204: "Supplier deleted", 404: "Supplier not found"}
    )
    def delete(self, request, supplier_id):
        supplier = generics.get_object_or_404(Supplier, supplier_id=supplier_id)
        supplier.delete()
        return Response({"message": "Supplier deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class WorkOrderCreateAPIView(generics.CreateAPIView):
    """
    Vista para crear una orden de trabajo.
    
    Se puede crear:
    1. Asociada a una incidencia: /suppliers/communities/{community_id}/claims/{claim_id}/work-orders/create/
    2. Independiente: /suppliers/communities/{community_id}/work-orders/create/
    """
    serializer_class = WorkOrderCreateSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="""
        Crea una nueva orden de trabajo.
        
        La orden puede estar asociada a una incidencia o ser independiente.
        Al crear la orden:
        - Se genera un número de orden único para la comunidad
        - Se crea una solicitud al proveedor automáticamente
        - Si está asociada a una incidencia, se genera un mensaje en la misma
        
        Ejemplo de payload:
        ```json
        {
            "title": "Reparación puerta garaje",
            "description": "La puerta no cierra correctamente",
            "supplier": "SUP-X7B2KM",
            "start_date": "2024-03-20T10:00:00Z"
        }
        ```
        """,
        request_body=WorkOrderCreateSerializer,
        responses={
            201: openapi.Response(
                description="Orden de trabajo creada correctamente",
                examples={
                    "application/json": {
                        "work_order_id": "550e8400-e29b-41d4-a716-446655440000",
                        "order_number": "WO-COM1-2024-0001",
                        "title": "Reparación puerta garaje",
                        "status": "pending",
                        "supplier_request_id": "550e8400-e29b-41d4-a716-446655440000"
                    }
                }
            ),
            400: "Datos inválidos",
            404: "Comunidad o incidencia no encontrada"
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        community = get_object_or_404(Community, community_id=self.kwargs['community_id'])
        claim = None
        if 'claim_id' in self.kwargs:
            claim = get_object_or_404(Claim, community=community, claim_id=self.kwargs['claim_id'])
        
        # Crear la orden de trabajo
        work_order = serializer.save(
            community=community,
            claim=claim,
            created_by=self.request.user
        )

        # Crear la solicitud al proveedor
        supplier_request = WorkOrderSupplierRequest.objects.create(
            work_order=work_order,
            supplier=work_order.supplier,
            expires_at=timezone.now() + timedelta(days=2)
        )

        # Actualizar el serializer con el request_id
        serializer.instance.supplier_request_id = supplier_request.request_id

        # Si la orden está vinculada a una incidencia, crear mensaje en la incidencia
        if claim:
            ClaimMessage.objects.create(
                claim=claim,
                user=self.request.user,
                message=f"Se ha creado la orden de trabajo {work_order.order_number} y enviado al proveedor {work_order.supplier.company_name}",
                message_type='work_order'
            )

        # Notificar al proveedor
        self._notify_supplier(supplier_request)

        return work_order

    def _notify_supplier(self, supplier_request):
        # Por ahora solo generamos el link de confirmación
        confirmation_link = f"{settings.SUPPLIER_PORTAL_URL}/work-orders/{supplier_request.request_id}/respond"
        print(f"Link de confirmación generado: {confirmation_link}")
        return confirmation_link

class WorkOrderSupplierResponseAPIView(generics.UpdateAPIView):
    """
    Vista para que los proveedores respondan a las solicitudes de trabajo.
    
    Endpoint: /suppliers/work-orders/requests/{request_id}/respond/
    """
    serializer_class = WorkOrderSupplierResponseSerializer
    lookup_field = 'request_id'
    queryset = WorkOrderSupplierRequest.objects.all()

    @swagger_auto_schema(
        operation_description="""
        Permite al proveedor responder a una solicitud de trabajo.
        
        El proveedor puede:
        - Aceptar la solicitud (debe proporcionar fecha de inicio)
        - Rechazar la solicitud (puede incluir motivo opcional)
        
        Ejemplos de payload:
        
        Aceptar:
        ```json
        {
            "status": "accepted",
            "start_date": "2024-03-20T10:00:00Z"
        }
        ```
        
        Rechazar:
        ```json
        {
            "status": "rejected",
            "rejection_reason": "No disponible en las fechas solicitadas"
        }
        ```
        """,
        request_body=WorkOrderSupplierResponseSerializer,
        responses={
            200: openapi.Response(
                description="Respuesta procesada correctamente",
                examples={
                    "application/json": {
                        "status": "accepted",
                        "start_date": "2024-03-20T10:00:00Z",
                        "message": "Respuesta registrada correctamente"
                    }
                }
            ),
            400: "Datos inválidos",
            404: "Solicitud no encontrada"
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="""
        Permite al proveedor responder a una solicitud de trabajo.
        Solo se actualizan los campos proporcionados.
        """,
        request_body=WorkOrderSupplierResponseSerializer,
        responses={
            200: "Respuesta actualizada correctamente",
            400: "Datos inválidos",
            404: "Solicitud no encontrada"
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    def perform_update(self, serializer):
        supplier_request = serializer.save(response_at=timezone.now())
        work_order = supplier_request.work_order

        if supplier_request.status == 'accepted':
            work_order.status = 'in_progress'
            work_order.start_date = serializer.validated_data.get('start_date')
            work_order.save()

            if work_order.claim:
                ClaimMessage.objects.create(
                    claim=work_order.claim,
                    user=work_order.created_by,
                    message=f"El proveedor {work_order.supplier.company_name} ha aceptado la orden de trabajo. Fecha prevista: {work_order.start_date.strftime('%d/%m/%Y')}",
                    message_type='work_order'
                )

            # Notificar al administrador y creador de la orden
            admin_users = work_order.community.get_admins_users()
            for admin_id in admin_users:
                admin = User.objects.get(id=admin_id)
                create_notification(
                    recipient=admin,
                    title="Orden de trabajo aceptada",
                    message=f"El proveedor {work_order.supplier.company_name} ha aceptado la orden de trabajo. Fecha prevista: {work_order.start_date.strftime('%d/%m/%Y')}",
                    link=f"{settings.FRONTEND_URL}/communities/{work_order.community.community_id}/work-orders/{work_order.work_order_id}"
                )

            # Notificar al creador si es diferente del admin
            if work_order.created_by.id not in admin_users:
                create_notification(
                    recipient=work_order.created_by,
                    title="Orden de trabajo aceptada", 
                    message=f"El proveedor {work_order.supplier.company_name} ha aceptado la orden de trabajo. Fecha prevista: {work_order.start_date.strftime('%d/%m/%Y')}",
                    link=f"{settings.FRONTEND_URL}/communities/{work_order.community.community_id}/work-orders/{work_order.work_order_id}"
                )

        elif supplier_request.status == 'rejected':
            work_order.status = 'rejected'
            work_order.save()

            if work_order.claim:
                admin_message = f"El proveedor {work_order.supplier.company_name} ha rechazado la orden de trabajo. "
                if supplier_request.rejection_reason:
                    admin_message += f"Motivo: '{supplier_request.rejection_reason}'"
                
                #Notificar al administrador y creador de la orden
                admin_users = work_order.community.get_admins_users()
                for admin_id in admin_users:
                    admin = User.objects.get(id=admin_id)

                    create_notification(
                        recipient=admin,
                        title="Orden de trabajo rechazada",
                        message = admin_message,
                        link=f"{settings.FRONTEND_URL}/communities/{work_order.community.community_id}/work-orders/{work_order.work_order_id}"
                    )

                ClaimMessage.objects.create(
                    claim=work_order.claim,
                    user=work_order.created_by,
                    message=f"El proveedor {work_order.supplier.company_name} ha rechazado la orden de trabajo. Se asignará a otro proveedor en breve.",
                    message_type='work_order'
                )

        elif supplier_request.status == 'completed':
            admin_users = work_order.community.get_admins_users()
            #Notificar al creador de la incidencia si no es admin
            if work_order.claim: 
                if work_order.created_by not in admin_users:
                    create_notification(
                        recipient=work_order.claim.created_by,
                        title="Orden de trabajo completada",
                        message=f"El proveedor {work_order.supplier.company_name} ha completado la orden de trabajo de la incidencia '{work_order.claim.title}'. Indica si la incidencia esta resuelta.",
                        link=f"{settings.FRONTEND_URL}/communities/{work_order.community.community_id}/claims/{work_order.claim.claim_id}"
                    )
                #Generar mensaje en la incidencia
                ClaimMessage.objects.create(
                    claim=work_order.claim,
                    user=work_order.created_by,
                    message=f"El proveedor {work_order.supplier.company_name} ha completado la orden de trabajo.",
                    message_type='work_order'
                )
            #Notificar al administrador

            for admin_id in admin_users:
                admin = User.objects.get(id=admin_id)

                create_notification(
                    recipient=admin,
                    title="Orden de trabajo completada",
                    message=f"El proveedor {work_order.supplier.company_name} ha completado la orden de trabajo.",
                    link=f"{settings.FRONTEND_URL}/communities/{work_order.community.community_id}/work-orders/{work_order.work_order_id}"
                )





                                    
