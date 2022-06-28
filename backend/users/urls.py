from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FollowUnfollowUser, GetSubscriptions

router = DefaultRouter()
router.register(
    r'^users/subscriptions/',
    GetSubscriptions,
)


urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:id>/subscribe/', FollowUnfollowUser.as_view()),
]
