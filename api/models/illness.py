from django.contrib.gis.db import models

class Illness(models.Model):
    sickness_name = models.CharField(max_length=200)