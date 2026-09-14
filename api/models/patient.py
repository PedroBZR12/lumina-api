from django.db import models
from api.models.responsible import Responsible
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
    cpf = models.CharField(max_length=15, null=False, blank=False)
    rg = models.CharField(max_length=15, null=False, blank=False)
    genre = models.IntegerField(choices=Genre.choices, null=False, blank=False)
    continuous_use_medicines = models.TextField()
    blood_type = models.IntegerField(choices=BloodType.choices)
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name="patient")
    hip = models.ForeignKey(HealthInsurancePlan, on_delete=models.CASCADE, related_name="patient") # health insurance plan
    temperament = models.CharField(max_length=100)
    hobbies = models.TextField(max_length=500)
    secondary_health_problems = models.TextField(max_length=400)
    responsible = models.ForeignKey(Responsible, on_delete=models.CASCADE, related_name="patient")
    # emergency_contact = models.CharField(max_length=50)
    # nationality = models.CharField(max_length=50)
    # allergies = models.TextField(blank=True, null=True)
    # restrictions = models.TextField(blank=True, null=True)
    # illnesses = models.TextField(blank=True, null=True)
    # id_register = models.CharField(max_length=9)
    # medical_history = models.TextField(blank=True, null=True)
    # vital_signs = models.TextField(blank=True, null=True)

    # caregiver = models.OneToOneField(Caregiver, on_delete=models.CASCADE, related_name="patient")
    # room_number = models.IntegerField()
    # last_pressure = models.CharField(max_length=20)