from rest_framework import serializers

from api.models import Responsible


class ResponsibleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Responsible
        fields = (
            'id', 'patient', 'complete_name', 'cpf', 'rg', 'birth_date',
            'email', 'main_cellphone', 'secondary_cellphone',
            'relationship_degree', 'emergency_contact', 'street', 'number',
            'complement', 'neighborhood', 'city', 'state', 'postal_code',
            'country',
        )
        extra_kwargs = {'patient': {'required': False}}

    def validate(self, attrs):
        patient = attrs.get('patient') or getattr(self.instance, 'patient', None)
        emergency = attrs.get(
            'emergency_contact',
            getattr(self.instance, 'emergency_contact', False),
        )
        if patient and not emergency and self.instance and self.instance.emergency_contact:
            if not patient.responsibles.filter(emergency_contact=True).exclude(
                pk=self.instance.pk
            ).exists():
                raise serializers.ValidationError(
                    {'emergency_contact': 'O paciente precisa manter um contato de emergência.'}
                )
        return attrs
