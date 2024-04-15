from django.urls import path
from .views import UserRegistrationAPIView, UserListAPIView, UserLoginAPIView, UserMainContactCommunityRegistrationAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('register-main-contact-community/', UserMainContactCommunityRegistrationAPIView.as_view(), name='register-main-contact-community'),


    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('', UserListAPIView.as_view(), name='user-list'),
]