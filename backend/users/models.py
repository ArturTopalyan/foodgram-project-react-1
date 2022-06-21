import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    is_blocked = models.BooleanField(
        default=False,
    )
    cart = models.ManyToManyField(
        'recipes.Recipe',
        related_name='carted'
    )
    favorite = models.ManyToManyField(
        'recipes.Recipe',
        related_name='favorites'
    )
    follow = models.ManyToManyField('self')
    REQUIRED_FIELDS = [
        'email',
        'first_name',
        'last_name',
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
