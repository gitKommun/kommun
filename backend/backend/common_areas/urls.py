from django.urls import path
from .views import CommonAreaListCreateAPIView, CommonAreaDetailAPIView, CommonAreaCreateAPIView, ReservationListAPIView, ReservationCreateAPIView, ReservationDeleteAPIView

urlpatterns = [


    path('<str:IDcommunity>/', CommonAreaListCreateAPIView.as_view(), name='list-create-common-area'), #GET/listar areas
    path('<str:IDcommunity>/create/', CommonAreaCreateAPIView.as_view(), name='common-area_create_api'),#POST/crear area comun
    path('<str:IDcommunity>/<int:area_id>/', CommonAreaDetailAPIView.as_view(), name='detail-common-area'), # GET/ver datos area, PUT/editar area, DELETE/borrar area

    path('<str:IDcommunity>/<int:common_area_id>/reservations/', ReservationListAPIView.as_view(), name='list-create-reservation'), #GET/listar reservas
    path('<str:IDcommunity>/<int:common_area_id>/reservations/create/', ReservationCreateAPIView.as_view(), name='list-create-reservation'), #GET/listar reservas
    path('<str:IDcommunity>/<int:common_area_id>/reservations/<int:reservation_id>/', ReservationDeleteAPIView.as_view(), name='detail-reservation'), #DELETE/borrar reserva

]
