from django.contrib.gis.db import models
from api.models import Patient

class Allergies(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='allergies')
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    reaction = models.TextField(max_length=400)
    trigger = models.TextField(max_length=300)
