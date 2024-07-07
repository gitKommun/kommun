from django.urls import path
from .views import ClaimCreateAPIView, ClaimListAPIView, ClaimCommentCreateAPIView, ClaimUpdateAPIView, ClaimDetailAPIView

urlpatterns = [
    path('<str:IDcommunity>/', ClaimListAPIView.as_view(), name='claims-list'),
    path('<str:IDcommunity>/create/', ClaimCreateAPIView.as_view(), name='claim-create'),
    path('<str:IDcommunity>/<int:pk>/', ClaimDetailAPIView.as_view(), name='claim-detail'),
    path('<str:IDcommunity>/<int:pk>/update/', ClaimUpdateAPIView.as_view(), name='claim-update'),
    path('<str:IDcommunity>/<int:claim_id>/add_comment/', ClaimCommentCreateAPIView.as_view(), name='claim-comment-create'),
]
