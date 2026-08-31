from django.contrib.gis.db import models

class Routine(models.Models):
    sleep_time = models.TimeField(null=False, blank=False)
    wakeup_time = models.TimeField(null=False, blank=False)
    bath_time = models.TimeField(null=False, blank=False)
