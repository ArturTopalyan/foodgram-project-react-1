from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import constraints

from tags.models import Tag

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        max_length=255,
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=255,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = (
            constraints.UniqueConstraint(
                fields=(
                    'name',
                    'measurement_unit',
                ),
                name='unique_name_measurement_unit',
            ),
        )

    def __str__(self):
        return '%(name)s, %(measurement_unit)s' % {
            'name': self.name,
            'measurement_unit': self.measurement_unit,
        }


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        help_text='Автор рецепта',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        'Название рецепта',
        unique=True,
        max_length=200,
    )
    image = models.ImageField(
        help_text='Фотография готового блюда.',
        upload_to='recipe/',
    )
    text = models.TextField(
        'Описание рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        help_text='тэги рецепта',
        related_name='tags',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        help_text='ингридиенты, необходимые для приготовления блюда',
        through='IngridientInRecipe',
        related_name='ingridients',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления блюда',
        validators=(
            MinValueValidator(
                1,
                'Укажите время, не меньшее, чем 1'
            ),
        )
    )
    pub_date = models.DateTimeField(
        'Время публикации рецепта',
        auto_now_add=True,
        editable=False,
        db_index=True,
    )

    class Meta:
        default_related_name = 'recipes'
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('user',)
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'
        default_related_name = 'favorites'
        constraints = (
            constraints.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite',
            ),
        )


class Cart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('id',)
        default_related_name = 'carts'
        verbose_name = 'рецепт в корзине'
        verbose_name_plural = 'рецепт в корзине'
        constraints = (
            constraints.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_cart',
            ),
        )


class IngridientInRecipe(models.Model):
    amount = models.PositiveIntegerField(
        'Количество ингридиента в рецепте',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('id',)
        default_related_name = 'ingridients_in_recipe'
        verbose_name = 'Ингридиент в рецепте'
        verbose_name_plural = 'Ингридиенты в рецепте'
        constraints = (
            constraints.UniqueConstraint(
                name='unique_amount_ingridients_recipe',
                fields=(
                    'recipe',
                    'ingredient',
                    'amount',
                ),
            ),
        )

    def __str__(self):
        return '%(amount)s %(mu)s %(ingridient)s в рецепте %(recipe)s' % {
            'amount': self.amount,
            'mu': self.ingredient.measurement_unit,
            'ingridient': self.ingredient.name,
            'recipe': self.recipe.name,
        }
