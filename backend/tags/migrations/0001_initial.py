# Generated by Django 3.2.13 on 2022-06-26 02:18

import colorfield.fields
import tags.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название')),
                ('color', colorfield.fields.ColorField(default='#FFFFFF', help_text='Цветовой HEX-код (например, #49B64E)', image_field=None, max_length=18, samples=None, unique=True)),
                ('slug', models.SlugField(unique=True, validators=[tags.validators.SlugValidator], verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('id',),
            },
        ),
    ]
