# Generated by Django 3.2.9 on 2022-07-10 07:17

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0009_auto_20220708_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_cat', to='items.category'),
        ),
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.FloatField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]