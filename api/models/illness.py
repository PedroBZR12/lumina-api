from django.db import models

class Illness(models.Model):
    sickness_name = models.CharField(max_length=200)