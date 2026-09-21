from django.db import models
from api.models.caregiver import CareGiver
from api.models.patient import Patient

class CaregiverPatient(models.Model):
    caregiver = models.ForeignKey(CareGiver, on_delete=models.CASCADE, related_name='patient')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='caregiver')
