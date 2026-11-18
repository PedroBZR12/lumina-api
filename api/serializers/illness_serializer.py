from rest_framework import serializers

from api.models import Illness


class IllnessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Illness
        fields = '__all__'
