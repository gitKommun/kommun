from django.urls import path
from .views import ClaimCreateAPIView, ClaimListAPIView, ClaimCommentCreateAPIView, ClaimUpdateAPIView, ClaimDetailAPIView, ClaimDeleteAPIView, ClaimCommentDeleteAPIView
from .views import CommunityClaimsListAPIView

urlpatterns = [
    path('<str:IDcommunity>/test', CommunityClaimsListAPIView.as_view(), name='claims-lisT'),
    path('<str:IDcommunity>/', ClaimListAPIView.as_view(), name='claims-list'),
    path('<str:IDcommunity>/create/', ClaimCreateAPIView.as_view(), name='claim-create'),
    path('<str:IDcommunity>/<int:claim_id>/', ClaimDetailAPIView.as_view(), name='claim-detail'),
    path('<str:IDcommunity>/<int:claim_id>/update/', ClaimUpdateAPIView.as_view(), name='claim-update'),
    path('<str:IDcommunity>/<int:claim_id>/add_comment/', ClaimCommentCreateAPIView.as_view(), name='claim-comment-create'),
    path('<str:IDcommunity>/<int:claim_id>/delete/', ClaimDeleteAPIView.as_view(), name='claim-delete'),
    path('<str:IDcommunity>/<int:claim_id>/<int:claim_comment_id>/delete/', ClaimCommentDeleteAPIView.as_view(), name='comment-delete'),
]
