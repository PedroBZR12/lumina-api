from django.db import models
from django.utils import timezone

from api.models.caregiver import CareGiver
from api.models.patient import Patient


class ClinicalRecord(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="clinical_records",
    )
    caregiver = models.ForeignKey(
        CareGiver,
        on_delete=models.PROTECT,
        related_name="clinical_records",
    )
    description = models.TextField()
    recorded_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ("recorded_at",)
