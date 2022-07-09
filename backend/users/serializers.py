from rest_framework import serializers

from recipes.utils import get_sub_exist

from .models import User


class UserGetSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        model = User

    def get_is_subscribed(self, obj: User):
        return get_sub_exist(
            request=self.context.get('request'),
            related_class='users.Follow',
            author__id=obj.id,
        )
