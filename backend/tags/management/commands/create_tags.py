import os
from csv import DictReader

from django.conf import settings as config
from django.core.management.base import BaseCommand
from tags.models import Tag

DATA_PATH = os.path.join(config.BASE_DIR, 'data/tags.csv')


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(DATA_PATH, newline='') as csvfile:
            reader = DictReader(
                csvfile,
                fieldnames=(
                    'name',
                    'color',
                    'slug',
                ),
            )
            for row in reader:
                Tag.objects.get_or_create(**row)
