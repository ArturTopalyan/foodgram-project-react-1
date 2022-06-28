from django.urls import path

from .views import FollowUnfollowUser

urlpatterns = [
    path('users/<int:id>/subscribe/', FollowUnfollowUser.as_view()),
]
