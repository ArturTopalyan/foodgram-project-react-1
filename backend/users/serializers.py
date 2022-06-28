from recipes.serializers import RecipeShortInfo
from recipes.utils import get_sub_exist
from rest_framework import serializers

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


class UserInSubscriptionsSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        model = User

    def get_recipes(self, obj):
        limit = self.context.get('kwargs').get('recipes_limit')
        return RecipeShortInfo(
            obj.recipes.all()[:limit],
            many=True
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()
