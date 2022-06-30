from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from tags.models import Tag
from tags.serializers import TagSerializer
from users.models import User
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


class IngredientRecipeSerializer(serializers.ModelSerializer):
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


class RecipeGetSerializer(serializers.ModelSerializer):
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True
    )
    is_favorited = serializers.SerializerMethodField(
        read_only=True
    )
    author = UserGetSerializer(
        read_only=True,
        many=False,
    )
    tags = TagSerializer(
        read_only=True,
        many=True,
    )
    ingredients = serializers.SerializerMethodField(
        read_only=True,
    )

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


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(
        many=True,
    )
    image = Base64ImageField(use_url=True, max_length=None)
    author = UserGetSerializer(
        read_only=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'author',
            'cooking_time',
        )

    def create_ingredients(self, recipe, ingredients):
        for ingredient in ingredients:
            IngridientInRecipe.objects.create(
                recipe=recipe,
                amount=ingredient['amount'],
                ingredient=ingredient['ingredient'],
            )

    @atomic
    def create(self, validated_data):
        request = self.context.get('request')
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=request.user,
            **validated_data
        )
        recipe.save()
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    @atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = instance
        IngridientInRecipe.objects.filter(recipe=instance).delete()
        self.create_ingredients(recipe, ingredients)
        return super().update(recipe, validated_data)

    def validate_ingredients(self, data):
        for ingredient in self.initial_data.get('ingredients'):
            if int(ingredient['amount']) < 1:
                raise serializers.ValidationError({
                    'ingredient': 'Количество ингридиента должно быть больше 1'
                })
        return data

    def validate_cooking_time(self, data):
        if self.initial_data.get('cooking_time') < 1:
            raise serializers.ValidationError({
                'cooking_time': 'Время приготовления должно быть больше 1'
            })
        return data

    def to_representation(self, instance):
        instance = Recipe.objects.get(id=instance.id)
        return RecipeGetSerializer(
            instance,
            context={
                'request': self.context.get('request'),
            }
        ).data


class RecipeShortInfo(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class UserInSubscriptionsSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

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
        read_only_fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def get_recipes(self, obj):
        print(self.get_extra_kwargs())
        return RecipeShortInfo(
            obj.recipes.all()[:6],
            many=True
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribed(self, obj):
        return get_sub_exist(
            request=self.context.get('request'),
            related_class='users.Follow',
            author__id=obj.id,
        )
