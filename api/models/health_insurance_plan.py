from django.db import models

class HealthInsurancePlan(models.Model):
    health_insurance_plan_name = models.CharField(max_length=100)
    membership_card_number = models.CharField(max_length=30)
    expiration_date = models.DateField(blank=False, null=False)