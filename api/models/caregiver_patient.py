from django.contrib.gis.db import models
from api.models import Patient, Caregiver
class CaregiverPatient(models.Model):
    caregiver = models.ForeignKey(Caregiver, on_delete=models.CASCADE, related_name='patient')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='caregiver')
