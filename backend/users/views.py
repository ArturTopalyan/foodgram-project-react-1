from django.shortcuts import get_object_or_404
from recipes.serializers import UserInSubscriptionsSerializer
from rest_framework import status
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Follow, User


class GetSubscriptions(GenericViewSet, ListModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserInSubscriptionsSerializer

    def get_queryset(self):
        return self.request.user.following.all()


class FollowUnfollowUser(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, user_id):
        Follow.objects.create(
            user=request.user,
            author=user_id,
        )
        user, _ = get_object_or_404(User, id=user_id)
        serializer = UserInSubscriptionsSerializer(
            user,
            many=False,
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                serializer,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {'error': 'somethink went wrong'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, user_id):
        if Follow.objects.filter(
            user=request.user,
            author=user_id,
        ).exists():
            Follow.objects.delete(
                user=request.user,
                author=user_id,
            )
            return Response(
                {'success': 'success'},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {'error': 'error'},
            status=status.HTTP_400_BAD_REQUEST,
        )
