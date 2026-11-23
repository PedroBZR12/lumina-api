from django.db import models
from api.models.routine import Routine
from api.models.health_insurance_plan import HealthInsurancePlan

class BloodType(models.IntegerChoices):
    A_PLUS = 1, "A+"
    A_MINUS = 2, "A-"
    B_PLUS = 3, "B+"
    B_MINUS = 4, "B-"
    AB_PLUS = 5, "AB+"
    AB_MINUS = 6, "AB-"
    O_PLUS = 7, "O+"
    O_MINUS = 8, "O-"

class Genre(models.IntegerChoices):
    MASCULINE = 1, "Masculino"
    FEMININE = 2, "Feminino"

class Patient(models.Model):
    complete_name = models.CharField(max_length=250)
    birth_date = models.DateField()
    main_diagnosis = models.TextField(null=False, blank=False, max_length=300)
    religion = models.CharField(max_length=50)
    cpf = models.CharField(max_length=15, null=False, blank=False, unique=True)
    rg = models.CharField(max_length=15, null=False, blank=False)
    genre = models.IntegerField(choices=Genre.choices, null=False, blank=False)
    continuous_use_medicines = models.TextField()
    blood_type = models.IntegerField(choices=BloodType.choices)
    routine = models.ForeignKey(Routine, on_delete=models.PROTECT, related_name="patient")
    hip = models.ForeignKey(
        HealthInsurancePlan,
        on_delete=models.SET_NULL,
        related_name="patient",
        null=True,
        blank=True,
    )
    temperament = models.CharField(max_length=100)
    hobbies = models.TextField(max_length=500)
    secondary_health_problems = models.TextField(max_length=400)

    @property
    def active(self):
        latest_admission = self.hospitalization_data.order_by(
            '-admission_datetime'
        ).first()
        return latest_admission is not None and latest_admission.discharge_date is None

    def delete(self, *args, **kwargs):
        raise RuntimeError(
            "Paciente nunca pode ser excluído; registre a data de alta."
        )