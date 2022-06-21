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
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingridient(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    measurement_unit = models.CharField(
        max_length=255,
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class IngridientRecipe(models.Model):
    amount = models.IntegerField()
    ingridient = models.ForeignKey(
        Ingridient,
        on_delete=models.CASCADE,
    )

    class Meta:
        default_related_name = 'ingridients'
        verbose_name = 'Ингридиент в рецепте'
        verbose_name_plural = 'Ингридиенты в рецепте'

    def __str__(self):
        return str(self.ingridient)


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
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
        Tag,
    )
    ingridients = models.ManyToManyField(
        IngridientRecipe,
    )
    cooking_time = models.IntegerField(
        validators=(
            MinValueValidator(
                1,
                'Укажите время, большее чем 1'
            ),
        )
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        ordering = ('-pub_date',)
        default_related_name = 'recipes'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name
