# Generated by Django 5.0.3 on 2024-04-13 09:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150)),
                ("author", models.CharField(max_length=260)),
                (
                    "cover",
                    models.CharField(
                        choices=[("status1", "HARD"), ("status2", "SOFT")],
                        default="status1",
                        max_length=20,
                    ),
                ),
                (
                    "inventory",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                ("daily_fee", models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
