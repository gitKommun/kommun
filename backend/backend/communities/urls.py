from django.urls import path
#from .views import CommunityListAPIView, AddUserToCommunityAPIView, CommunityUsersAPIView, ManageUserCommunityRoleAPIView, CommunityCreateAPIView, CommunityDeleteAPIView, CommunityUserListAPIView
#from .views import PersonCommunityListAPIView, PersonCommunityDetailAPIView, PersonCommunityCreateAPIView, CommunityUserRolesAPIView, BulkPersonCommunityUploadAPIView
#from .views import community_detail, community_update, ManageUserRolesAPIView

from .views import CommunityCreateAPIView, community_detail, community_update, CommunityDeleteAPIView
from .views import ListPersonCommunityAPIView, AddMultiplePersonCommunityAPIView, get_person_community, update_person_community, delete_person_community

urlpatterns = [
    #path('', CommunityUserListAPIView.as_view(), name='community_list'), #GET/listar comunidades

    #Community URLS 
    path('create/', CommunityCreateAPIView.as_view(), name='community-create'), #POST/crear comunidad
    path('<str:IDcommunity>/', community_detail, name='community-detail'), #GET/ver datos comunidad
    path('<str:IDcommunity>/update/', community_update, name='community-update'), #POST/editar comunidad
    path('<str:IDcommunity>/delete/', CommunityDeleteAPIView.as_view(), name='community-delete'), #DELETE/borrar comunidad
    

    #Neighbors URLS / PersonCommunity = Cada persona asociada a la comunidad, tenga cuenta de usuario o no. 
    path('<str:IDcommunity>/neighbors/', ListPersonCommunityAPIView.as_view(), name='person-usercommunity-list'), #GET/listar personas asociadas a la comunidad
    
    path('<str:IDcommunity>/neighbors/add/', AddMultiplePersonCommunityAPIView.as_view(), name='add-neighbors-bulk'),
    path('<str:IDcommunity>/neighbors/<int:person_id>/', get_person_community, name='get-person-community'),
    path('<str:IDcommunity>/neighbors/<int:person_id>/update/', update_person_community, name='update-person-community'),
    path('<str:IDcommunity>/neighbors/<int:person_id>/delete/', delete_person_community, name='delete-person-community'),

]