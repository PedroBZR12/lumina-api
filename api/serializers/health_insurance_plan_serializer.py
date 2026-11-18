from rest_framework import serializers

from api.models import HealthInsurancePlan


class HealthInsurancePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthInsurancePlan
        fields = '__all__'
