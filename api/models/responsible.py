from django.db import models

class Responsible(models.Model):
    complete_name = models.CharField(max_length=200, null=False, blank=False)
    cpf = models.CharField(max_length=15)
    rg = models.CharField(max_length=15)
    birth_date = models.DateField(null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    main_cellphone = models.CharField(max_length=15, null=False, blank=False)
    secondary_cellphone = models.CharField(max_length=15, null=True, blank=True)
