from django.db import models
from colorfield.fields import ColorField
from .validators import SlugValidator

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
        ordering = ('id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
