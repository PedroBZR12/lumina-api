from django.db import models

class Routine(models.Model):
    sleep_time = models.TimeField(null=False, blank=False)
    wakeup_time = models.TimeField(null=False, blank=False)
    bath_time = models.TimeField(null=False, blank=False)
