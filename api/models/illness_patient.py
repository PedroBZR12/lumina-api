from django.contrib.gis.db import models
from api.models import Patient, Illness

class IllnessPatient(models.Model):
    illness = models.ForeignKey(Illness)
    patient = models.ForeignKey(Patient)