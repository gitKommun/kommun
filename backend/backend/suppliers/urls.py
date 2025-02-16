from django.urls import path
from .views import (
    SupplierListAPIView,
    SupplierCreateAPIView,
    SupplierRetrieveAPIView,
    SupplierUpdateAPIView,
    SupplierDeleteAPIView,
)

urlpatterns = [
    path('', SupplierListAPIView.as_view(), name='supplier-list'),
    path('create/', SupplierCreateAPIView.as_view(), name='supplier-create'),
    path('<uuid:supplier_id>/', SupplierRetrieveAPIView.as_view(), name='supplier-detail'),
    path('<uuid:supplier_id>/update/', SupplierUpdateAPIView.as_view(), name='supplier-update'),
    path('<uuid:supplier_id>/delete/', SupplierDeleteAPIView.as_view(), name='supplier-delete'),
]
