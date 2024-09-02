from django.urls import path
from .views import CommunityListAPIView, AddUserToCommunityAPIView, CommunityUsersAPIView, ManageUserCommunityRoleAPIView, CommunityCreateAPIView, CommunityDeleteAPIView, CommunityUserListAPIView
from .views import PersonCommunityListAPIView, PersonCommunityDetailAPIView, PersonCommunityCreateAPIView, CommunityUserRolesAPIView, BulkPersonCommunityUploadAPIView
from .views import community_detail, community_update, ManageUserRolesAPIView
urlpatterns = [
    path('', CommunityUserListAPIView.as_view(), name='community_list'), #GET/listar comunidades

    #Community URLS OK
    path('create/', CommunityCreateAPIView.as_view(), name='community-create'), #POST/crear comunidad
    path('<str:IDcommunity>/', community_detail, name='community-detail'), #GET/ver datos comunidad
    path('<str:IDcommunity>/update/', community_update, name='community-update'), #POST/editar comunidad
    path('<str:IDcommunity>/delete/', CommunityDeleteAPIView.as_view(), name='community-delete'), #DELETE/borrar comunidad
    

    #Neighbors = UserCommunityRole, es el punto de conexion entre los vecinos y la comunidad, registrados o no en la plataforma. La clase User y Person no se conecta 
    #directamente a la comunidad, se conecta a traves de la clase UserCommunityRole(Neighbors)

    #Neighbor URLS / UserCommunityRole = Cada persona asociada a la comunidad, tenga cuenta de usuario o no. 
    path('<str:IDcommunity>/neighbors/', CommunityUserRolesAPIView.as_view(), name='person-usercommunity-list'), #GET/listar personas asociadas a la comunidad
    path('<str:IDcommunity>/neighbors/upload_neighbors_bulk/', BulkPersonCommunityUploadAPIView.as_view(), name='upload-person-bulk'),

    #User URLS / Users = Persona que tiene una cuenta de acceso a la plataforma, 
    #path('<str:IDcommunity>/users/', CommunityUsersAPIView.as_view(), name='community-users-list'),
    #path('<str:IDcommunity>/add-user/', AddUserToCommunityAPIView.as_view(), name='add-user-to-community'), #POST/crear usuario + asignar rol
    
    path('<str:IDcommunity>/manage-roles/<int:neighbour_id>/', ManageUserRolesAPIView.as_view(), name='manage-user-roles'),
    #path('<str:IDcommunity>/manage-role/', ManageUserCommunityRoleAPIView.as_view(), name='manage-user-role'), #POST/Añadir rol a usuario
    #path('<str:IDcommunity>/manage-role/<int:role_id>/', ManageUserCommunityRoleAPIView.as_view(), name='update-delete-user-role'),#PUT/DELETE/Modificar-eliminar rol

    #Person URLS / Person = Registro de informacion de los datos de una persona, solo registro de los datos, no es una cuenta activa
    #path('<str:IDcommunity>/people/', PersonCommunityListAPIView.as_view(), name='personcommunity-list'), #GET/listar personas de la comunidad
    #path('<str:IDcommunity>/people/create/', PersonCommunityCreateAPIView.as_view(), name='personcommunity-create'), #POST/crear persona
    #path('<str:IDcommunity>/people/<int:person_id>/', PersonCommunityDetailAPIView.as_view(), name='personcommunity-detail') #GET/ver datos persona, PUT/editar persona, DELETE/borrar persona

]