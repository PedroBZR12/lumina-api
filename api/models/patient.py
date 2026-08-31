from django.contrib.gis.db import models
from api.models import Caregiver, Responsable


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
    1 = "M"
    2 = "F"

class Patient(models.Models):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    cpf = models.CharField(max_length=15)
    rg = models.CharField(max_length=15)
    genre = models.IntegerChoices(Genre.choices)
    religion = models.CharField(max_length=30)
    blood_type = models.IntegerChoices(BloodType.choices)

    emergency_contact = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    hip = models.CharField(max_length=200) # health insurance plan
    routine = models.TextField()
    temperament = models.CharField(max_length=100)
    hobby = models.CharField(max_length=100)
    allergies = models.TextField(blank=True, null=True)
    restrictions = models.TextField(blank=True, null=True)
    continuous_use_medicines = models.TextField()
    illnesses = models.TextField(blank=True, null=True)
    id_register = models.CharField(max_length=9)
    medical_history = models.TextField(blank=True, null=True)
    vital_signs = models.TextField(blank=True, null=True)

    caregiver = models.OneToOneField(Caregiver, on_delete=models.CASCADE, related_name="patient")
    responsible = models.OneToOneField(Responsable, on_delete=models.CASCADE, related_name="responsible")
    room_number = models.IntegerField()
    last_pressure = models.CharField(max_length=20)