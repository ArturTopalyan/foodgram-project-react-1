import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import constraints

from .managers import CustomUserManager


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    is_blocked = models.BooleanField(
        default=False,
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        help_text='Адрес электронной почты'
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )

    objects = CustomUserManager()

    REQUIRED_FIELDS = (
        'email',
        'first_name',
        'last_name',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


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
