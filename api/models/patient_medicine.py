from django.db import models
from api.models.patient import Patient
from api.models.medicine import Medicine
from api.models.caregiver import CareGiver

class PatientMedicine(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medicine')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='patient')
    dosage = models.CharField(max_length=10)
    last_hour = models.TimeField(blank=True, null=True)
    daily_frequency = models.CharField(blank=False, null=False)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    last_worker_gives_dosage = models.ForeignKey(CareGiver, on_delete=models.CASCADE)