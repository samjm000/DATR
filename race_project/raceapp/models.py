# raceapp/models.py

from django.db import models


class Racecard(models.Model):
    name = models.CharField(max_length=255)


class Race(models.Model):
    racecard = models.ForeignKey(
        Racecard, on_delete=models.CASCADE, related_name="races"
    )
    link = models.URLField()
    title = models.CharField(max_length=255)
    details = models.TextField()


class Horse(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="horses")
    name = models.CharField(max_length=255)
    link = models.URLField()
    sire = models.CharField(max_length=255)
    dam = models.CharField(max_length=255)
    dams_sire = models.CharField(max_length=255)
