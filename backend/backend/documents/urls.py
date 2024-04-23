from django.urls import path
from .views import FolderListAPIView, FolderCreateAPIView

urlpatterns = [
    path('folders/', FolderListAPIView.as_view(), name='folder_list_api'),
    path('folder_create/', FolderCreateAPIView.as_view(), name='folder_create_api'),
]