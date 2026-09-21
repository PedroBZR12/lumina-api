from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api.models.caregiver import CareGiver

class CareGiverSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
    )
    
    class Meta:
        model = CareGiver
        fields = (
            'id',
            'complete_name',
            'cpf',
            'email',
            'shift_start_time',
            'shift_end_time',
            'pause_time',
            'cellphone',
            'password',
        )
        read_only_fields = (
            'id',
        )

    def create(self, validated_data):
            password = validated_data.pop('password', None)
            if password:
                validated_data["password"] = make_password(password)
                return CareGiver.objects.create(**validated_data)
            raise serializers.ValidationError("A instância não possui valores corretos.")

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.clientPasswordHash = make_password(password)

        instance.save()

        return instance