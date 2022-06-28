import os
from csv import DictReader

from django.conf import settings as config
from django.core.management.base import BaseCommand
from recipes.models import Ingredient

DATA_PATH = os.path.join(config.BASE_DIR, '../data/ingredients.csv')


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(DATA_PATH, newline='') as csvfile:
            reader = DictReader(
                csvfile,
                fieldnames=('name', 'measurement_unit'),
            )
            for row in reader:
                Ingredient.objects.get_or_create(**row)
