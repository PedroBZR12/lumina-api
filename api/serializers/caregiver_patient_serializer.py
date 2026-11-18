from rest_framework import serializers

from api.models import CaregiverPatient


class CaregiverPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaregiverPatient
        fields = '__all__'
        read_only_fields = ('caregiver',)
