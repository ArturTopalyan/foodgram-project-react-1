from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import constraints

from colorfield.fields import ColorField

from .validators import SlugValidator

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        unique=True,
    )
    color = ColorField(
        help_text='Цветовой HEX-код (например, #49B64E)',
        unique=True,
    )
    slug = models.SlugField(
        'slug',
        unique=True,
        validators=(
            SlugValidator,
        ),
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingridient(models.Model):
    name = models.CharField(
        'Название',
        max_length=255,
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=255,
    )

    class Meta:
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
        related_name='recipes',
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
        through='TagInRecipe',
    )
    ingridients = models.ManyToManyField(
        Ingridient,
        help_text='ингридиенты, необходимые для приготовления блюда',
        through='IngridientInRecipe',
    )
    cooking_time = models.IntegerField(
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
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = (
            constraints.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow_user_author',
            ),
        )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='followers',
    )

    class Meta:
        constraints = (
            constraints.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite',
            ),
        )


class Cart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='carts',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='carts',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            constraints.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_cart',
            ),
        )


class IngridientInRecipe(models.Model):
    amount = models.IntegerField(
        'Количество ингридиента в рецепте',
        validators=(
            MinValueValidator(
                limit_value=0,
            ),
        )
    )
    ingridient = models.ForeignKey(
        Ingridient,
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingridient',
    )

    class Meta:
        verbose_name = 'Ингридиент в рецепте'
        verbose_name_plural = 'Ингридиенты в рецепте'

    def __str__(self):
        return '%(amount)s %(ingridient)s' % {
            'amount': self.amount,
            'ingridient': self.ingridient,
        }


class TagInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        Tag,
        related_name='recipes',
        on_delete=models.CASCADE,
    )
