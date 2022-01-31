from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from src.apps.car.querysets import CarQuerySet


class Car(models.Model):
    make = models.CharField(max_length=256)
    model = models.CharField(max_length=256)

    objects = CarQuerySet.as_manager()

    def __str__(self):
        return f"{self.make} - {self.model}"


class Rate(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="rates")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
