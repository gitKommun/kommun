from django.urls import path
from .views import CreateVoteAPIView, CastVoteAPIView, VoteDetailAPIView, UpdateVoteAPIView, DeleteVoteAPIView

urlpatterns = [
    path('<str:IDcommunity>/create/', CreateVoteAPIView.as_view(), name='create-vote'),
    path('<str:IDcommunity>/polls/<int:vote_id>/vote/', CastVoteAPIView.as_view(), name='cast-vote'),

    path('<str:IDcommunity>/polls/<int:vote_id>/details/', VoteDetailAPIView.as_view(), name='vote-detail'),
    path('<str:IDcommunity>/polls/<int:vote_id>/update/', UpdateVoteAPIView.as_view(), name='update-vote'),
    path('<str:IDcommunity>/polls/<int:vote_id>/delete/', DeleteVoteAPIView.as_view(), name='delete-vote'),
]
