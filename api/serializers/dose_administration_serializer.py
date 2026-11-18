from django.utils import timezone
from rest_framework import serializers

from api.models import DoseAdministration


class DoseAdministrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoseAdministration
        fields = (
            'id', 'prescription', 'scheduled_at', 'status', 'caregiver',
            'recorded_at',
        )
        read_only_fields = ('status', 'caregiver', 'recorded_at')

    def validate(self, attrs):
        prescription = attrs.get(
            'prescription',
            getattr(self.instance, 'prescription', None),
        )
        scheduled_at = attrs.get(
            'scheduled_at',
            getattr(self.instance, 'scheduled_at', None),
        )
        if prescription and scheduled_at:
            scheduled_date = timezone.localtime(scheduled_at).date()
            if not prescription.start_date <= scheduled_date <= prescription.end_date:
                raise serializers.ValidationError(
                    {'scheduled_at': 'A dose deve estar dentro do período da prescrição.'}
                )
            duplicate = DoseAdministration.objects.filter(
                prescription=prescription,
                scheduled_at=scheduled_at,
            )
            if self.instance:
                duplicate = duplicate.exclude(pk=self.instance.pk)
            if duplicate.exists():
                raise serializers.ValidationError(
                    {'scheduled_at': 'Já existe uma dose neste horário.'}
                )
        return attrs
