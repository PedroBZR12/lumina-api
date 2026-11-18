from rest_framework import serializers

from api.models import Allergies


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergies
        fields = '__all__'
