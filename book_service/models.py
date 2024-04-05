from django.db import models
from django.core.validators import MinValueValidator


class Book(models.Model):

    cover_choice = {
        "status1": "HARD",
        "status2": "SOFT",
    }

    title = models.CharField(max_length=150)
    author = models.CharField(max_length=260)
    cover = models.CharField(max_length=20, choices=cover_choice, default="status1")
    inventory = models.IntegerField(validators=(MinValueValidator(0), ))
    daily_fee = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return f"{self.title} - {self.author}"
