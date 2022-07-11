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
        db_index=True,
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def blocked(self):
        return not self.is_blocked


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers',
    )

    class Meta:
        ordering = ('id',)
        constraints = (
            constraints.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follow_user_author',
            ),
            constraints.CheckConstraint(
                check=~models.Q(author=models.F('user')),
                name='author_is_not_follower',
            ),
        )

    def __str__(self):
        return '%(user)s following %(author)s' % {
            'user': self.user,
            'author': self.author,
        }
