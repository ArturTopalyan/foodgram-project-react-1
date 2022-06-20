from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


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
        upload_to='recipe',
    )
    description = models.TextField(
        'Описание'
    )
    time = models.DateTimeField(
        'Время публикации рецепта',
        auto_now_add=True,
    )

    class Meta:
        default_related_name = 'recipes'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
