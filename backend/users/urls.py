from django.urls import path

from .views import FollowUnfollowUser

urlpatterns = [
    path(
        'users/<slug:id>/subscribe/',
        FollowUnfollowUser.as_view(),
        'users_follow',
    ),
]
