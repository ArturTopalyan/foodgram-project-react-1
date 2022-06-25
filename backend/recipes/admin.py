from django.contrib import admin

from . import models


@admin.register(models.TagInRecipe)
class TagInRecipeAdmin(admin.ModelAdmin):
    fields = (
        'tag',
        'recipe',
    )


@admin.register(models.Ingridient)
class IngridientAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )
    empty_value_display = '-пусто-'


@admin.register(models.IngridientInRecipe)
class IngridientInRecipeAdmin(admin.ModelAdmin):
    fields = (
        'ingridient',
        'recipe',
        'amount',
    )


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = (
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
    )
    list_display = (
        'name',
        'author',
    )
    filter_horizontal = (
        'ingridients',
        'tags',
    )
    list_filter = (
        'author',
        'name',
        'ingridients',
        'tags',
    )


@admin.register(models.Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'recipe',
    )


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    fields = (
        'recipe',
        'user',
    )
