from django.db import transaction
from rest_framework import serializers

from api.models import HospitalizationData, Patient, Responsible
from api.serializers.responsible_serializer import ResponsibleSerializer
from api.serializers.validators import normalize_cpf


class AdmissionInputSerializer(serializers.Serializer):
    room = serializers.CharField(max_length=50)
    main_diagnosis = serializers.CharField(max_length=600)
    admission_datetime = serializers.DateTimeField(required=False)


class PatientSerializer(serializers.ModelSerializer):
    responsibles = ResponsibleSerializer(many=True)
    admission = AdmissionInputSerializer(write_only=True, required=False)
    active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Patient
        fields = (
            'id', 'complete_name', 'birth_date', 'main_diagnosis', 'religion',
            'cpf', 'rg', 'genre', 'continuous_use_medicines', 'blood_type',
            'routine', 'hip', 'temperament', 'hobbies',
            'secondary_health_problems', 'responsibles', 'admission', 'active',
        )

    def validate_cpf(self, value):
        value = normalize_cpf(value)
        queryset = Patient.objects.filter(cpf=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('Este CPF já está cadastrado.')
        return value

    def validate_responsibles(self, responsibles):
        if not responsibles:
            raise serializers.ValidationError(
                'Cadastre ao menos um responsável para o paciente.'
            )
        if not any(contact.get('emergency_contact', False) for contact in responsibles):
            raise serializers.ValidationError(
                'Ao menos um responsável deve ser contato de emergência.'
            )
        return responsibles

    @transaction.atomic
    def create(self, validated_data):
        responsibles = validated_data.pop('responsibles')
        admission = validated_data.pop('admission', None)
        if admission is None:
            raise serializers.ValidationError(
                {'admission': 'Informe os dados da admissão inicial.'}
            )
        patient = Patient.objects.create(**validated_data)
        for contact in responsibles:
            contact.pop('id', None)
            contact.pop('patient', None)
            Responsible.objects.create(patient=patient, **contact)
        HospitalizationData.objects.create(
            patient=patient,
            caregiver=self.context['request'].user,
            **admission,
        )
        return patient

    @transaction.atomic
    def update(self, instance, validated_data):
        responsibles = validated_data.pop('responsibles', None)
        if validated_data.pop('admission', None) is not None:
            raise serializers.ValidationError(
                {'admission': 'Atualize admissões pelo endpoint de internações.'}
            )
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        if responsibles is not None:
            for contact in responsibles:
                contact_id = contact.pop('id', None)
                related_patient = contact.pop('patient', None)
                if related_patient and related_patient.pk != instance.pk:
                    raise serializers.ValidationError(
                        {'responsibles': 'O responsável deve pertencer a este paciente.'}
                    )
                if contact_id:
                    updated_count = Responsible.objects.filter(
                        pk=contact_id,
                        patient=instance,
                    ).update(**contact)
                    if not updated_count:
                        raise serializers.ValidationError(
                            {'responsibles': 'Responsável inválido para este paciente.'}
                        )
                else:
                    Responsible.objects.create(patient=instance, **contact)
        return instance
