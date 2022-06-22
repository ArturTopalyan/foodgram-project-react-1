import uuid
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.core.exceptions import FieldError
from django.apps import apps



class CustomUserManager(UserManager):
    def _create_user(
        self,
        username,
        email,
        password,
        first_name,
        last_name,
        **extra_fields,
    ):
        requred_fields = {
            'username должен быть указан': username,
            'email должен быть указан': email,
            'password должен быть указан': password,
            'first_name должен быть указан': first_name,
            'last_name должен быть указан': last_name,
        }
        for message, field in requred_fields.items():
            if field is None:
                raise FieldError(message)
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label,
            self.model._meta.object_name,
        )
        username = GlobalUserModel.normalize_username(username)
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        username=None,
        email=None,
        password=None,
        first_name=None,
        last_name=None,
        **extra_fields,
    ):
        false_fields = (
            'is_staff',
            'is_superuser',
            'is_blocked',
        )
        for field in false_fields:
            extra_fields.setdefault(field, False)
        return self._create_user(
            username,
            email,
            password,
            first_name,
            last_name,
            **extra_fields,
        )

    def create_superuser(
        self,
        username=None,
        email=None,
        password=None,
        first_name=None,
        last_name=None,
        **extra_fields
    ):
        true_fields = (
            'is_staff',
            'is_superuser',
        )
        for field in true_fields:
            extra_fields.setdefault(field, True)
        extra_fields.setdefault('is_blocked', False)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(
            username,
            email,
            password,
            first_name,
            last_name,
            **extra_fields,
        )


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
        'Имя пользователя',
        max_length=150,
    )
    last_name = models.CharField(
        'Фамилия пользователя',
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
