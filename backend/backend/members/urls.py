from django.urls import path
from .views import UserLoginView, UserRegistrationAPIView, UserListAPIView, UserMainContactCommunityRegistrationAPIView, get_user_email, get_user_data,UserLogoutAPIView

urlpatterns = [
    #Finales
    
    path('register/', UserMainContactCommunityRegistrationAPIView.as_view(), name='register-main-contact-community'),

    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user-logout'),


    path('me/', get_user_data, name='get_user_data'),

    #Temporales para el desarrollo
    path('', UserListAPIView.as_view(), name='user-list'),
    path('user_email/', get_user_email, name='get_user_email'),
    #path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
]