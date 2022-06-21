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


@admin.register(models.Ingridient)
class IngridientAdmin(admin.ModelAdmin):
    fields = (
        'name',
        'measurement_unit',
    )
    empty_value_display = '-пусто-'


@admin.register(models.IngridientRecipe)
class IngridientRecipeAdmin(admin.ModelAdmin):
    fields = (
        'amount',
        'ingridient',
    )
    empty_value_display = '-пусто-'


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = (
        'author',
        'name',
        'image',
        'tags',
        'ingridients',
        'text',
        'cooking_time',
    )
    list_filter = (
        'author',
        'tags',
        'name',
    )
    empty_value_display = '-пусто-'
