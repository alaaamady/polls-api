from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PollViewSet, VoteViewSet, VoteConfirmationView

router = DefaultRouter()
router.register(r'polls', PollViewSet)
router.register(r'vote', VoteViewSet, basename='vote')


urlpatterns = [
    path('', include(router.urls)),
    path('confirm_vote', VoteConfirmationView.as_view())
]
