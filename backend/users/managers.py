from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.core.exceptions import FieldError


class CustomUserManager(UserManager):
    """
    Менеджер нужен из-за переопределения необходимых полей.
    Теперь, если полей будет не достаточно, то пользователь не создастся.
    """

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
        global_user_model = apps.get_model(
            self.model._meta.app_label,
            self.model._meta.object_name,
        )
        username = global_user_model.normalize_username(username)
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
