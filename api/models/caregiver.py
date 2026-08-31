from django.contrib.gis.db import models
from django.contrib.auth.models import User

class CareGiver(models.Models):
    complete_name = models.CharField(max_length=200, null=False, blank=False)
    cpf = models.CharField(max_length=15, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    shift_start_time = models.TimeField(null=False, blank=False)
    shift_end_time = models.TimeField(null=False, blank=False)
    pause_time = models.TimeField(null=False, blank=False)
    cellphone = models.CharField(max_length=30)

