from django.urls import path

from .views import PropertyUpdateAPIView, list_properties, PropertyCreateAPIView, PropertyDeleteAPIView, BulkUploadPropertiesView, BulkCreatePropertiesFromCatastroAPIView, DeleteAllPropertiesAPIView
from .views import CreatePropertyRelationshipAPIView, DeletePropertyRelationshipAPIView


urlpatterns = [
    #Property URLS O
    path('<str:IDcommunity>/', list_properties, name='list-properties'), #GET/listar propiedades

    path('<str:IDcommunity>/create/', PropertyCreateAPIView.as_view(), name='add-property'), #POST/añadir propiedad
    path('<str:IDcommunity>/<int:property_id>/update/', PropertyUpdateAPIView.as_view(), name='edit-property'),#PUT/editar propiedad
    path('<str:IDcommunity>/<int:property_id>/delete/', PropertyDeleteAPIView.as_view(), name='delete-property'),#DELETE/borrar propiedad
    path('<str:IDcommunity>/delete-properties/', DeleteAllPropertiesAPIView.as_view(), name='delete_all_properties'),#DELETE/borrar TODAS las propiedades


    path('<str:IDcommunity>/upload-properties/', BulkUploadPropertiesView.as_view(), name='upload-properties'), #POST/ carga masiva de propiedades con excel
    path('<str:IDcommunity>/load-properties-API/', BulkCreatePropertiesFromCatastroAPIView.as_view(), name='create-properties-from-catastro'), #POST/ carga masiva de propiedades con excel


    #Property relationship URLS
    path('<str:IDcommunity>/property-relationship/create/', CreatePropertyRelationshipAPIView.as_view(), name='create-property-relationship'), #POST/crear relacion
    path('<str:IDcommunity>/property-relationship/delete/', DeletePropertyRelationshipAPIView.as_view(), name='delete-property-relationship'), #DELETE/borrar
]






