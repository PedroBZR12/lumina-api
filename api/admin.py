from django.contrib import admin
from api.models import CaregiverPatient


@admin.register(CaregiverPatient)
class CaregiverPatientAdmin(admin.ModelAdmin):
    list_display = ("caregiver", "patient")
    list_filter = ("caregiver",)
    search_fields = ("caregiver__complete_name", "patient__complete_name")
