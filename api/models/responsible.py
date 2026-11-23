from django.db import models
from api.models.patient import Patient

class Responsible(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="responsibles")
    complete_name = models.CharField(max_length=200, null=False, blank=False)
    cpf = models.CharField(max_length=15)
    rg = models.CharField(max_length=15)
    birth_date = models.DateField(null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    main_cellphone = models.CharField(max_length=15, null=False, blank=False)
    secondary_cellphone = models.CharField(max_length=15, null=True, blank=True)
    relationship_degree = models.CharField(max_length=50, default="Não informado")
    emergency_contact = models.BooleanField(default=False)
    street = models.CharField(max_length=150, blank=True, default="")
    number = models.CharField(max_length=20, blank=True, default="")
    complement = models.CharField(max_length=100, blank=True, default="")
    neighborhood = models.CharField(max_length=100, blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")
    state = models.CharField(max_length=2, blank=True, default="")
    postal_code = models.CharField(max_length=9, blank=True, default="")
    country = models.CharField(max_length=80, blank=True, default="")
