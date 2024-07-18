from django.urls import path
from .views import CommunityListAPIView, AddUserToCommunityAPIView, CommunityUsersAPIView, ManageUserCommunityRoleAPIView
from .views import PersonCommunityListAPIView, PersonCommunityDetailAPIView, PersonCommunityCreateAPIView
from .views import community_detail, community_update, list_properties, add_property_to_community, edit_property, delete_property, add_property_to_community2
urlpatterns = [
    path('', CommunityListAPIView.as_view(), name='community_list'), #GET/listar comunidades

    #Community URLS
    path('<str:IDcommunity>/', community_detail, name='community-detail'), #GET/ver datos comunidad
    path('<str:IDcommunity>/update/', community_update, name='community-update'), #POST/editar comunidad
    
    #Property URLS
    path('<str:IDcommunity>/properties/', list_properties, name='list-properties'), #GET/listar propiedades
    path('<str:IDcommunity>/addProperty/', add_property_to_community2, name='add-property'), #POST/añadir propiedad
    path('<str:IDcommunity>/properties/<int:property_id>/edit/', edit_property, name='edit-property'),#PUT/editar propiedad
    path('<str:IDcommunity>/properties/<int:property_id>/delete/', delete_property, name='delete-property'),#DELETE/borrar propiedad

    #User URLS
    path('<str:IDcommunity>/users/', CommunityUsersAPIView.as_view(), name='community-users-list'),
        #AÑADIR datos del usuario
    path('<str:IDcommunity>/add-user/', AddUserToCommunityAPIView.as_view(), name='add-user-to-community'), #POST/crear usuario + asignar rol
    path('<str:IDcommunity>/manage-role/', ManageUserCommunityRoleAPIView.as_view(), name='manage-user-role'), #POST/Añadir rol a usuario
    path('<str:IDcommunity>/manage-role/<int:role_id>/', ManageUserCommunityRoleAPIView.as_view(), name='update-delete-user-role'),#PUT/DELETE/Modificar-eliminar rol

    #Person URLS
    path('<str:IDcommunity>/people/', PersonCommunityListAPIView.as_view(), name='personcommunity-list'), #GET/listar personas de la comunidad
    path('<str:IDcommunity>/people/create/', PersonCommunityCreateAPIView.as_view(), name='personcommunity-create'), #POST/crear persona
    path('<str:IDcommunity>/people/<int:person_id>/', PersonCommunityDetailAPIView.as_view(), name='personcommunity-detail') #GET/ver datos persona, PUT/editar persona, DELETE/borrar persona

    #TO DO: URLS para gestionar creacion de User + UserCommunityRole desde PersonCommunity

]