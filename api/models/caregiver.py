from django.contrib.gis.db import models
from django.contrib.auth.models import User

class CareGiver(models.Models):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='caregiver_profile')
    cellphone = models.CharField(max_length=30)

