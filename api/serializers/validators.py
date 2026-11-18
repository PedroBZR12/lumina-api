import re

from rest_framework import serializers


def normalize_cpf(value):
    cpf = re.sub(r"\D", "", value)
    if len(cpf) != 11:
        raise serializers.ValidationError("Informe um CPF com 11 dígitos.")
    return cpf
