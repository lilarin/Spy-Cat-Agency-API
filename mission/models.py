from django.core.validators import MaxLengthValidator
from django.db import models, transaction
from cat.models import SpyCat
from django.core.exceptions import ValidationError


class Mission(models.Model):
    cat = models.OneToOneField(
        SpyCat, null=True, blank=True, on_delete=models.CASCADE
    )
    completed = models.BooleanField(default=False)

    def clean(self):
        if self.cat and self.cat.mission and not self.cat.mission.completed:
            raise ValidationError("A cat can only have one active mission.")

    def __str__(self):
        return f"Mission {self.id}"


class Target(models.Model):
    mission = models.ForeignKey(
        Mission, related_name="targets", on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=100, validators=[MaxLengthValidator(100)]
    )
    country = models.CharField(
        max_length=100, validators=[MaxLengthValidator(100)]
    )
    notes = models.TextField()
    completed = models.BooleanField(default=False)

    def clean(self):
        if self.mission and self.mission.targets.count() >= 3:
            raise ValidationError("A mission can only have up to 3 targets.")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            if self.mission:
                all_completed = all(
                    target.completed for target in self.mission.targets.all()
                )
                if all_completed:
                    self.mission.completed = True
                else:
                    self.mission.completed = False
                self.mission.save()

    def __str__(self):
        return self.name
