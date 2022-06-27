from rest_framework import serializers

from .models import Ingredient, IngridientInRecipe, Recipe
from .utils import get_sub_exist


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        source='ingredient',
    )

    class Meta:
        model = IngridientInRecipe
        fields = (
            'id',
            'amount',
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_in_shopping_cart(self, obj):
        return get_sub_exist(
            request=self.context.get('request'),
            sub='recipes.Cart',
            recipe=obj,
        )

    def get_is_favorited(self, obj):
        return get_sub_exist(
            request=self.context.get('request'),
            sub='recipes.Favorite',
            recipe=obj,
        )
