from rest_framework import serializers
from tags.serializers import TagSerializer
from users.serializers import UserGetSerializer

from .models import Ingredient, IngridientInRecipe, Recipe
from .utils import get_sub_exist


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        read_only=True
    )
    measurement_unit = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='measurement_unit',
        read_only=True,
    )
    name = serializers.SlugRelatedField(
        source='ingredient',
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = IngridientInRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeGetSerializer(serializers.ModelSerializer):
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    author = UserGetSerializer(
        read_only=True,
        many=False,
    )
    tags = TagSerializer(
        read_only=True,
        many=True,
    )
    ingredients = serializers.SerializerMethodField()

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

    def get_ingredients(self, obj):
        return IngredientInRecipeSerializer(
            obj.ingridients_in_recipe.all(),
            many=True,
        ).data

    def get_is_in_shopping_cart(self, obj):
        return get_sub_exist(
            request=self.context.get('request'),
            related_class='recipes.Cart',
            recipe=obj,
        )

    def get_is_favorited(self, obj):
        return get_sub_exist(
            request=self.context.get('request'),
            related_class='recipes.Favorite',
            recipe=obj,
        )
