from django.contrib.gis.db import models
from api.models import Caregiver, Patient
class HospitalizationData(models.Model):
    date = models.DateField(null=False, blank=False, auto_created=True)
    hour = models.DateField(null=False, blank=False, auto_created=True)
    room = models.CharField(null=False, blank=False)
    caregiver = models.ForeignKey(Caregiver)
    patient = models.ForeignKey(Patient)
    main_diagnosis = models.TextField(max_length=600)