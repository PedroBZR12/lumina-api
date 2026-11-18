from rest_framework import serializers

from api.models import IllnessPatient


class IllnessPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = IllnessPatient
        fields = '__all__'
