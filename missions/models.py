from django.db import models
from cats.models import SpyCat


class Mission(models.Model):
    cat = models.OneToOneField(SpyCat, null=True, blank=True, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Mission {self.id}"


class Target(models.Model):
    mission = models.ForeignKey(
        Mission, related_name="targets", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    notes = models.TextField()
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name
