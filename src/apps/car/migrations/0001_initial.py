# Generated by Django 4.0 on 2022-01-27 23:14

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Car",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("make", models.CharField(max_length=256)),
                ("model", models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name="Rate",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ]
                    ),
                ),
                (
                    "car",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="rates", to="car.car"),
                ),
            ],
        ),
    ]
