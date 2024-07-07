from django.urls import path
from .views import (
    VoteCreateAPIView,
    VoteListAPIView,
    VoteDetailAPIView,
    VoteUpdateDeleteAPIView,
    OptionCreateAPIView,
    OptionListAPIView,
    OptionDetailAPIView,
    OptionUpdateDeleteAPIView,
    VoteRecordCreateAPIView,
    VoteRecordListAPIView
)

urlpatterns = [
    # Vote URLs
    path('<str:IDcommunity>/', VoteListAPIView.as_view(), name='vote-list'),
    path('<str:IDcommunity>/create/', VoteCreateAPIView.as_view(), name='vote-create'),
    path('<str:IDcommunity>/<int:vote_id>/', VoteDetailAPIView.as_view(), name='vote-detail'),
    path('<str:IDcommunity>/<int:vote_id>/update-delete/', VoteUpdateDeleteAPIView.as_view(), name='vote-update-delete'),
    
    # Option URLs
    path('<str:IDcommunity>/<int:vote_id>/options/', OptionListAPIView.as_view(), name='option-list'),
    path('<str:IDcommunity>/<int:vote_id>/options/create/', OptionCreateAPIView.as_view(), name='option-create'),
    path('<str:IDcommunity>/<int:vote_id>/options/<int:option_id>/', OptionDetailAPIView.as_view(), name='option-detail'),
    path('<str:IDcommunity>/<int:vote_id>/options/<int:option_id>/update-delete/', OptionUpdateDeleteAPIView.as_view(), name='option-update-delete'),
    
    # VoteRecord URLs
    path('<str:IDcommunity>/<int:vote_id>/records/', VoteRecordListAPIView.as_view(), name='voterecord-list'),
    path('<str:IDcommunity>/<int:vote_id>/records/create/', VoteRecordCreateAPIView.as_view(), name='voterecord-create'),
]
