from django.contrib.gis.db import models

class Responsible(models.Models):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_lenght=50)
    cpf = models.CharField(max_length=15)
    birth_date = models.DateField()
    email = models.EmailField()
    cellphone = models.CharField(max_length=20)
    address = models.TextField(max_length=50)
