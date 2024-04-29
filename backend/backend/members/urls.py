from django.urls import path
from .views import UserLoginView, UserRegistrationAPIView, UserListAPIView, UserLoginAPIView, UserMainContactCommunityRegistrationAPIView,  UserLogoutAPIView
from .views import get_user_email, get_user_data


urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('register_user_community/', UserMainContactCommunityRegistrationAPIView.as_view(), name='register-main-contact-community'),

    path('login/', UserLoginView.as_view(), name='user-login'),
    path('', UserListAPIView.as_view(), name='user-list'),

    path('logout/', UserLogoutAPIView.as_view(), name='user-logout'),

    path('user_email/', get_user_email, name='get_user_email'),

    path('userData/', get_user_data, name='user_data'),

]