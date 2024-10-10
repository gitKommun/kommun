from django.urls import path
from .views import UserLoginView, UserRegistrationAPIView, UserListAPIView, get_user_data, UserLogoutAPIView, UserUpdateAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register-main-contact-community'), #POST/registrar usuario y crear una comunidad vacia

    path('login/', UserLoginView.as_view(), name='user-login'), #POST/iniciar sesión
    path('logout/', UserLogoutAPIView.as_view(), name='user-logout'), #POST/cerrar sesión

    path('me/', get_user_data, name='get_user_data'), #GET/ ver datos usuario
    path('me/update/', UserUpdateAPIView.as_view(), name='user-update'), #PUT/ actualizar datos usuario

    #Temporales para el desarrollo
    path('', UserListAPIView.as_view(), name='user-list'),
    #path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
]