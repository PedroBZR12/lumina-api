from rest_framework import serializers

from api.models import HospitalizationData


class HospitalizationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalizationData
        fields = (
            'id', 'patient', 'caregiver', 'admission_datetime',
            'discharge_date', 'room', 'main_diagnosis',
        )
        read_only_fields = ('caregiver',)

    def validate(self, attrs):
        discharge_date = attrs.get(
            'discharge_date',
            getattr(self.instance, 'discharge_date', None),
        )
        admission_datetime = attrs.get(
            'admission_datetime',
            getattr(self.instance, 'admission_datetime', None),
        )
        if (
            discharge_date
            and admission_datetime
            and discharge_date < admission_datetime.date()
        ):
            raise serializers.ValidationError(
                {'discharge_date': 'A alta não pode anteceder a admissão.'}
            )
        if self.instance and self.instance.discharge_date and not discharge_date:
            raise serializers.ValidationError(
                {'discharge_date': 'A alta registrada não pode ser removida.'}
            )
        return attrs
