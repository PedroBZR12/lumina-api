from rest_framework import serializers

from api.models import Allergies


class AllergySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Allergies
        fields = ('id', 'patient', 'type', 'name', 'reaction', 'trigger')
        extra_kwargs = {'patient': {'required': False}}
