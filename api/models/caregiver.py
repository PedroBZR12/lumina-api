from django.db import models

class CareGiver(models.Model):
    complete_name = models.CharField(max_length=200, null=False, blank=False)
    cpf = models.CharField(max_length=15, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    shift_start_time = models.TimeField(null=False, blank=False)
    shift_end_time = models.TimeField(null=False, blank=False)
    pause_time = models.TimeField(null=False, blank=False)
    cellphone = models.CharField(max_length=30)
    password = models.CharField(max_length=100)

