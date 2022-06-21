from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from .validators import HexColorValidator

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        max_length=7,
        validators=[HexColorValidator],
        unique=True,
    )
    slug = models.SlugField(
        unique=True
    )
    REQUIRED_FIELDS = (
        'name',
        'color',
        'slug',
    )


class IngridientRecipe(models.Model):
    amount = models.IntegerField()
    ingridient = models.ForeignKey(
        'Ingridient',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        'Recipe',
        on_delete=models.CASCADE
    )

    class Meta:
        default_related_name = 'ingridients'


class Ingridient(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    measurement_unit = models.CharField(
        max_length=255,
    )


class Recipe(models.Model):
    author = models.ForeignKey(
        'users.User',
        help_text='Автор рецепта',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        'Название',
        unique=True,
        max_length=200,
    )
    image = models.ImageField(
        upload_to='recipe/',
    )
    text = models.TextField(
        'Описание'
    )
    tags = models.ManyToManyField(
        'Tag',
    )
    ingridients = models.ManyToManyField(
        'IngridientInRecipe',
    )
    cooking_time = models.IntegerField(
        validators=(
            MinValueValidator(
                1,
                'Укажите время, большее чем 1'
            ),
        )
    )

    class Meta:
        default_related_name = 'recipes'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
