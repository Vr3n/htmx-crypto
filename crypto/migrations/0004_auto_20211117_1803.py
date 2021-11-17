# Generated by Django 3.2.9 on 2021-11-17 18:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crypto', '0003_auto_20211117_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='bought_currency_fee',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=19, validators=[django.core.validators.MaxValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sold_currency_amount',
            field=models.DecimalField(decimal_places=10, max_digits=19, validators=[django.core.validators.MaxValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='sold_currency_fee',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=19, validators=[django.core.validators.MaxValueValidator(0)]),
        ),
    ]
