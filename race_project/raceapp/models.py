from django.db import models

# Create your models here.
from django.db import models


class Race(models.Model):
    date = models.DateField()
    location = models.CharField(max_length=100)
    time = models.TimeField()
    name = models.CharField(max_length=200)
    race_class = models.CharField(max_length=10)
    age_group = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.date} - {self.name} at {self.location}"


class Horse(models.Model):
    race = models.ForeignKey(Race, related_name="horses", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    sire = models.CharField(max_length=100)
    dam = models.CharField(max_length=100)
    di_number = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} (Sire: {self.sire}, Dam: {self.dam})"


class Pedigree(models.Model):
    horse_name = models.CharField(max_length=100)
    di_number = models.FloatField(null=True, blank=True)
    info = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.horse_name} - DI: {self.di_number}"
