from django.db import models
from api.models.caregiver import CareGiver
from api.models.patient import Patient

class HospitalizationData(models.Model):
    date = models.DateField(null=False, blank=False, auto_created=True)
    hour = models.DateField(null=False, blank=False, auto_created=True)
    room = models.CharField(null=False, blank=False)
    caregiver = models.ForeignKey(CareGiver, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    main_diagnosis = models.TextField(max_length=600)