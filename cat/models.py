from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class SpyCat(models.Model):
    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1), MaxValueValidator(20)
        ]
    )
    breed = models.CharField(max_length=100)
    salary = models.DecimalField(
        max_digits=6, decimal_places=2,
        validators=[
            MinValueValidator(0.1)
        ]
    )

    def __str__(self):
        return self.name
