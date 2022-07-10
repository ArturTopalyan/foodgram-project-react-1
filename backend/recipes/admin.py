from django.contrib import admin

from . import models


class IngredientInLine(admin.TabularInline):
    model = models.IngridientInRecipe
    extra = 0


class TagInline(admin.TabularInline):
    model = models.Recipe.tags.through
    extra = 0


@admin.register(models.Ingredient)
class IngridientAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )
    empty_value_display = '-пусто-'


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
        'tags',
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    inlines = (
        IngredientInLine,
        TagInline
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
