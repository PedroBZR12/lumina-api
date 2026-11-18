from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api.models import CareGiver
from api.serializers.validators import normalize_cpf


class CareGiverSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CareGiver
        fields = (
            'id', 'complete_name', 'cpf', 'email', 'shift_start_time',
            'shift_end_time', 'pause_time', 'cellphone', 'password',
        )

    def validate_email(self, value):
        queryset = CareGiver.objects.filter(email__iexact=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('Este e-mail já está cadastrado.')
        return value

    def validate_cpf(self, value):
        value = normalize_cpf(value)
        queryset = CareGiver.objects.filter(cpf=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('Este CPF já está cadastrado.')
        return value

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
        return super().update(instance, validated_data)
