from django.db import models

class Routine(models.Model):
    sleep_time = models.TimeField(null=False, blank=False)
    wakeup_time = models.TimeField(null=False, blank=False)
    bath_time = models.TimeField(null=False, blank=False)
    breakfast_time = models.TimeField(null=True, blank=True)
    lunch_time = models.TimeField(null=True, blank=True)
    dinner_time = models.TimeField(null=True, blank=True)
