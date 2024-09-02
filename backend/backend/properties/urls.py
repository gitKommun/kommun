from django.urls import path

from .views import PropertyUpdateAPIView, list_properties, PropertyCreateAPIView, PropertyDeleteAPIView, BulkUploadPropertiesView
urlpatterns = [
    #Property URLS OK
    path('<str:IDcommunity>/properties/', list_properties, name='list-properties'), #GET/listar propiedades
    path('<str:IDcommunity>/properties/create/', PropertyCreateAPIView.as_view(), name='add-property'), #POST/añadir propiedad
    path('<str:IDcommunity>/properties/<int:property_id>/update/', PropertyUpdateAPIView.as_view(), name='edit-property'),#PUT/editar propiedad
    path('<str:IDcommunity>/properties/<int:property_id>/delete/', PropertyDeleteAPIView.as_view(), name='delete-property'),#DELETE/borrar propiedad
    path('<str:IDcommunity>/properties/upload-properties/', BulkUploadPropertiesView.as_view(), name='upload-properties'), #POST/ carga masiva de propiedades con excel
    #TODO: Manage properties ownership relations
]




