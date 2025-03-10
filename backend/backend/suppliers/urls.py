from django.urls import path
from . import views

app_name = 'suppliers'

urlpatterns = [
    path('', views.SupplierListAPIView.as_view(), name='supplier-list'),
    path('create/', views.SupplierCreateAPIView.as_view(), name='supplier-create'),
    path('<uuid:supplier_id>/', views.SupplierRetrieveAPIView.as_view(), name='supplier-detail'),
    path('<uuid:supplier_id>/update/', views.SupplierUpdateAPIView.as_view(), name='supplier-update'),
    path('<uuid:supplier_id>/delete/', views.SupplierDeleteAPIView.as_view(), name='supplier-delete'),

    path('<str:community_id>/work-orders/create/', 
         views.WorkOrderCreateAPIView.as_view(), 
         name='work-order-create'),
    path('<str:community_id>/claims/<int:claim_id>/work-orders/create/', 
         views.WorkOrderCreateAPIView.as_view(), 
         name='claim-work-order-create'),

    path('work-orders/requests/<uuid:request_id>/respond/',
         views.WorkOrderSupplierResponseAPIView.as_view(),
         name='work-order-supplier-response'),
]
