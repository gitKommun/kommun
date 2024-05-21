from django.urls import path
from .views import FolderListAPIView, FolderCreateAPIView, FolderDetailAPIView

urlpatterns = [
    path('<str:IDcommunity>/folders/', FolderListAPIView.as_view(), name='folder_list_api'), #GET/listar carpetas
    path('<str:IDcommunity>/folder_create/', FolderCreateAPIView.as_view(), name='folder_create_api'),#POST/crear carpeta
    path('<str:IDcommunity>/folder/<str:IDfolder>/delete/', FolderDetailAPIView.as_view(), name='folder_delete_api'),#DELETE/borrar carpeta
    path('<str:IDcommunity>/folder/<str:IDfolder>/update/', FolderDetailAPIView.as_view(), name='folder_update_api'),#PUT/actualizar

    
]