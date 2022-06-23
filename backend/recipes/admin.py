from django.contrib import admin

from . import models


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'color',
        'slug',
    )
    empty_value_display = '-пусто-'


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
    empty_value_display = '-пусто-'


@admin.register(models.IngridientInRecipe)
class IngridientInRecipeAdmin(admin.ModelAdmin):
    fields = (
        'ingridient',
        'recipe',
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
    filter_horizontal = (
        'ingridients',
        'tags',
    )
    list_filter = (
        'author',
        'name',
    )
    empty_value_display = '-пусто-'


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
