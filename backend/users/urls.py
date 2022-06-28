from django.urls import path

from .views import FollowUnfollowUser

urlpatterns = [
    path('users/<str:id>/subscribe/', FollowUnfollowUser.as_view()),
]
