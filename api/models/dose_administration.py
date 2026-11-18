from django.db import models
from api.models.caregiver import CareGiver
from api.models.patient_medicine import PatientMedicine


class DoseStatus(models.TextChoices):
    PENDING = "PENDENTE", "Pendente"
    ADMINISTERED = "MINISTRADO", "Ministrado"
    REFUSED = "RECUSADO", "Recusado"


class DoseAdministration(models.Model):
    prescription = models.ForeignKey(
        PatientMedicine,
        on_delete=models.CASCADE,
        related_name="scheduled_doses",
    )
    scheduled_at = models.DateTimeField()
    status = models.CharField(
        max_length=12,
        choices=DoseStatus.choices,
        default=DoseStatus.PENDING,
    )
    caregiver = models.ForeignKey(
        CareGiver,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="dose_administrations",
    )
    recorded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("scheduled_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("prescription", "scheduled_at"),
                name="unique_prescription_dose_time",
            ),
        ]
