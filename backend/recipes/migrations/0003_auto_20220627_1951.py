# Generated by Django 3.2.13 on 2022-06-27 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20220626_0538'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ingridientinrecipe',
            name='unique_amount_ingridients_recipe',
        ),
        migrations.RenameField(
            model_name='ingridientinrecipe',
            old_name='ingridient',
            new_name='ingredient',
        ),
        migrations.AddConstraint(
            model_name='ingridientinrecipe',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient', 'amount'), name='unique_amount_ingridients_recipe'),
        ),
    ]
