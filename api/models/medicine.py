from django.contrib.gis.db import models

class Medicine(models.Model):
    medicine_name = models.CharField(max_length=200)