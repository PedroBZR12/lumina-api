from django.contrib.gis.db import models
from api.models import Caregiver, Responsable, Routine


class BloodType(models.IntegerChoices):
    1 = "A+"
    2 = "A-"
    3 = "B+"
    4 = "B-"
    5 = "AB+"
    6 = "AB-"
    7 = "O+"
    8 = "O-"

class Genre(models.IntegerChoices):
    1 = "Masculino"
    2 = "Feminino"

class Patient(models.Models):
    complete_name = models.CharField(max_length=250)
    birth_date = models.DateField()
    main_diagnosis = models.TextField(null=False, blank=False, max_length=300)
    religion = models.CharField(max_length=50)
    cpf = models.CharField(max_length=15, null=False, blank=False)
    rg = models.CharField(max_length=15, null=False, blank=False)
    genre = models.IntegerChoices(Genre.choices, null=False, blank=False)
    continuous_use_medicines = models.TextField()
    blood_type = models.IntegerChoices(BloodType.choices)
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name="patient")
    hip = models.ForeignKey() # health insurance plan
    temperament = models.CharField(max_length=100)
    hobbies = models.TextField(max_length=500)
    secondary_health_problems = models.TextField(max_length=400)
    responsible = models.ForeignKey(Responsable, on_delete=models.CASCADE, related_name="responsible")
    hospitalization_data = models
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