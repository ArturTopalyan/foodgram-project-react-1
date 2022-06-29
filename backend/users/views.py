from django.shortcuts import get_object_or_404
from recipes.serializers import UserInSubscriptionsSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Follow, User


class FollowUnfollowUser(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        Follow.objects.get_or_create(
            user=request.user,
            author=user,
        )
        serializer = UserInSubscriptionsSerializer(
            user,
            many=False,
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, id):
        if Follow.objects.filter(
            user=request.user,
            author=id,
        ).exists():
            Follow.objects.delete(
                user=request.user,
                author=id,
            )
            return Response(
                {'success': 'success'},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {'error': 'error'},
            status=status.HTTP_400_BAD_REQUEST,
        )
