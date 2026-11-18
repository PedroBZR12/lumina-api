from rest_framework import serializers

from api.models import PatientMedicine


class PatientMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientMedicine
        fields = '__all__'
        read_only_fields = ('last_hour', 'last_worker_gives_dosage')
