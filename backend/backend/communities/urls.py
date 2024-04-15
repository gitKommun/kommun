from django.urls import path
from .views import CommunityListAPIView

urlpatterns = [
    path('', CommunityListAPIView.as_view(), name='community_list'),
]