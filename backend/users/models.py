import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    REQUIRED_FIELDS = [
        'email',
        'first_name',
        'last_name',
    ]

    @property
    def blocked(self):
        return not self.is_active
