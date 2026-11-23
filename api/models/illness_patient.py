from django.db import models
from api.models.patient import Patient
from api.models.illness import Illness

class IllnessPatient(models.Model):
    illness = models.ForeignKey(Illness, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("illness", "patient"),
                name="unique_patient_illness",
            ),
        ]