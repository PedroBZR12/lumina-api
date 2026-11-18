from django.db import models
from django.utils import timezone
from api.models.caregiver import CareGiver
from api.models.patient import Patient

class HospitalizationData(models.Model):
    admission_datetime = models.DateTimeField(default=timezone.now)
    discharge_date = models.DateField(null=True, blank=True)
    room = models.CharField(max_length=50, null=False, blank=False)
    caregiver = models.ForeignKey(CareGiver, on_delete=models.PROTECT)
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="hospitalization_data",
    )
    main_diagnosis = models.TextField(max_length=600)