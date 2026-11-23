from django.db import models
from api.models.patient import Patient

class AllergyType(models.TextChoices):
    MEDICATION = "MEDICAMENTO", "Medicamento"
    FOOD = "ALIMENTAR", "Alimentar"
    OTHER = "OUTRA", "Outra"

class Allergies(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='allergies')
    type = models.CharField(max_length=20, choices=AllergyType.choices)
    name = models.CharField(max_length=200)
    reaction = models.TextField(max_length=400)
    trigger = models.TextField(max_length=300)
