from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Supplier
from .serializers import SupplierSerializer

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
