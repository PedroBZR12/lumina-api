from rest_framework.viewsets import ModelViewSet
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from api.models import CaregiverPatient, Patient
from api.serializers import PatientSerializer


class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.select_related("routine", "hip").prefetch_related(
        "responsibles", "hospitalization_data"
    )
    serializer_class = PatientSerializer

    def get_queryset(self):
        queryset = self.queryset.filter(
            caregiver__caregiver=self.request.user
        ).distinct()
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(complete_name__icontains=name)
        return queryset

    @transaction.atomic
    def perform_create(self, serializer):
        patient = serializer.save()
        CaregiverPatient.objects.create(
            caregiver=self.request.user,
            patient=patient,
        )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "Paciente não pode ser excluído; registre a alta."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )