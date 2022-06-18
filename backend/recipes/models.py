from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        help_text='Автор рецепта',
        on_delete=models.CASCADE,
        verbose_name='Автор',
        verbose_name_plural='Авторы',
    )
    name = models.CharField(
        'Название',
        max_length=200,
        verbose_name='Название',
        verbose_name_plural='Названия',
    )
    image = models.ImageField(
        upload_to='recipe',
        verbose_name='Изображение',
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
