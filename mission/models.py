from django.core.validators import MaxLengthValidator
from django.db import models
from cat.models import SpyCat
from django.core.exceptions import ValidationError


class Mission(models.Model):
    cat = models.OneToOneField(SpyCat, null=True, blank=True, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(completed=False) | models.Q(cat__mission__isnull=True),
                name="only_one_active_mission_per_cat"
            )
        ]

    def __str__(self):
        return f"Mission {self.id}"


class Target(models.Model):
    mission = models.ForeignKey(
        Mission, related_name="targets", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100, validators=[MaxLengthValidator(100)])
    country = models.CharField(max_length=100, validators=[MaxLengthValidator(100)])
    notes = models.TextField()
    completed = models.BooleanField(default=False)

    def clean(self):
        if self.mission and self.mission.targets.count() >= 3:
            raise ValidationError("A mission can only have up to 3 targets.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
