from rest_framework import serializers
from api.models.patient import  Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            'complete_name',
            'birth_date',
            'main_diagnosis',
            'religion',
            'cpf',
            'rg',
            'genre',
            'continuous_use_medicines',
            'blood_type',
            'routine',
            'hip',
            'temperament',
            'hobbies',
        )
        read_only_fields = ('id')