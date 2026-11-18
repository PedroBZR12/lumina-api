from rest_framework import serializers

from api.models import ClinicalRecord


class ClinicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalRecord
        fields = ('id', 'patient', 'caregiver', 'description', 'recorded_at')
        read_only_fields = ('caregiver', 'recorded_at')
