from django.urls import path
from .views import FolderListAPIView, FolderCreateAPIView, FolderDetailAPIView, FolderOpenAPIView
from .views import DocumentUploadAPIView, DocumentDetailAPIView, DocumentDeleteAPIView, DocumentDownloadAPIView, RootFolderAndDocumentsAPIView

urlpatterns = [
    path('<str:IDcommunity>/', RootFolderAndDocumentsAPIView.as_view(), name='root_folders_and_documents_api'),#GET/listar carpetas con numero de elementos + documentos en ROOT

    path('<str:IDcommunity>/folders/', FolderListAPIView.as_view(), name='folder_list_api'), #GET/listar carpetas con numero de elementos
    path('<str:IDcommunity>/folders/create/', FolderCreateAPIView.as_view(), name='folder_create_api'),#POST/crear carpeta

    path('<str:IDcommunity>/folders/<str:IDfolder>/', FolderOpenAPIView.as_view(), name='folder_detail_api'),#GET/ver carpeta
    path('<str:IDcommunity>/folders/<str:IDfolder>/delete/', FolderDetailAPIView.as_view(), name='folder_delete_api'),#DELETE/borrar carpeta
    path('<str:IDcommunity>/folders/<str:IDfolder>/update/', FolderDetailAPIView.as_view(), name='folder_update_api'),#PUT/actualizar

    path('<str:IDcommunity>/f/<int:IDfolder>/upload/', DocumentUploadAPIView.as_view(), name='document-upload'), #POST/subir documento
    path('<str:IDcommunity>/d/<int:IDdocument>/', DocumentDetailAPIView.as_view(), name='document-detail'), #GET/ver documento
    path('<str:IDcommunity>/d/<int:IDdocument>/download/', DocumentDownloadAPIView.as_view(), name='document-download'), #GET/descargar documento
    path('<str:IDcommunity>/d/<int:IDdocument>/delete/', DocumentDeleteAPIView.as_view(), name='document-delete'), #DELETE/borrar documento

]