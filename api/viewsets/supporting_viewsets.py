from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_date
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.models import (
    Allergies,
    CareGiver,
    CaregiverPatient,
    ClinicalRecord,
    DoseAdministration,
    DoseStatus,
    HealthInsurancePlan,
    HospitalizationData,
    Illness,
    IllnessPatient,
    Medicine,
    PatientMedicine,
    Responsible,
    Routine,
)
from api.serializers import (
    AllergySerializer,
    CareGiverSerializer,
    CaregiverPatientSerializer,
    ClinicalRecordSerializer,
    DoseAdministrationSerializer,
    HealthInsurancePlanSerializer,
    HospitalizationDataSerializer,
    IllnessPatientSerializer,
    IllnessSerializer,
    MedicineSerializer,
    PatientMedicineSerializer,
    ResponsibleSerializer,
    RoutineSerializer,
)


class CareGiverViewSet(ModelViewSet):
    queryset = CareGiver.objects.all()
    serializer_class = CareGiverSerializer

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]


class AssignedPatientsMixin:
    def get_queryset(self):
        return super().get_queryset().filter(
            patient__caregiver__caregiver=self.request.user
        ).distinct()

    def require_assigned_patient(self, patient):
        if not CaregiverPatient.objects.filter(
            patient=patient,
            caregiver=self.request.user,
        ).exists():
            raise PermissionDenied("O paciente não está vinculado a este cuidador.")

    def perform_create(self, serializer):
        self.require_assigned_patient(serializer.validated_data["patient"])
        serializer.save()

    def perform_update(self, serializer):
        patient = serializer.validated_data.get(
            "patient",
            serializer.instance.patient,
        )
        self.require_assigned_patient(patient)
        serializer.save()

class ResponsibleViewSet(AssignedPatientsMixin, ModelViewSet):
    queryset = Responsible.objects.select_related("patient")
    serializer_class = ResponsibleSerializer

    def perform_create(self, serializer):
        patient = serializer.validated_data.get("patient")
        if patient is None:
            raise ValidationError({"patient": "Este campo é obrigatório."})
        self.require_assigned_patient(patient)
        serializer.save()

    def perform_update(self, serializer):
        patient = serializer.validated_data.get(
            "patient",
            serializer.instance.patient,
        )
        self.require_assigned_patient(patient)
        serializer.validated_data.pop("id", None)
        serializer.save()

    def perform_destroy(self, instance):
        if instance.patient.responsibles.count() <= 1:
            raise ValidationError(
                "O paciente precisa manter ao menos um responsável."
            )
        if instance.emergency_contact and not instance.patient.responsibles.exclude(
            pk=instance.pk
        ).filter(emergency_contact=True).exists():
            raise ValidationError(
                "O paciente precisa manter ao menos um contato de emergência."
            )
        instance.delete()


class AllergyViewSet(AssignedPatientsMixin, ModelViewSet):
    queryset = Allergies.objects.select_related("patient")
    serializer_class = AllergySerializer


class HospitalizationDataViewSet(AssignedPatientsMixin, ModelViewSet):
    queryset = HospitalizationData.objects.select_related("patient", "caregiver")
    serializer_class = HospitalizationDataSerializer
    http_method_names = ("get", "post", "put", "patch", "head", "options")

    def perform_create(self, serializer):
        patient = serializer.validated_data["patient"]
        self.require_assigned_patient(patient)
        serializer.save(caregiver=self.request.user)


class HealthInsurancePlanViewSet(ModelViewSet):
    queryset = HealthInsurancePlan.objects.all()
    serializer_class = HealthInsurancePlanSerializer


class RoutineViewSet(ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer


class IllnessViewSet(ModelViewSet):
    queryset = Illness.objects.all()
    serializer_class = IllnessSerializer


class IllnessPatientViewSet(AssignedPatientsMixin, ModelViewSet):
    queryset = IllnessPatient.objects.select_related("patient", "illness")
    serializer_class = IllnessPatientSerializer

    def perform_create(self, serializer):
        patient = serializer.validated_data["patient"]
        self.require_assigned_patient(patient)
        serializer.save()


class MedicineViewSet(ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class PatientMedicineViewSet(AssignedPatientsMixin, ModelViewSet):
    queryset = PatientMedicine.objects.select_related(
        "patient", "medicine", "last_worker_gives_dosage"
    )
    serializer_class = PatientMedicineSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        patient_id = self.request.query_params.get("patient")
        if patient_id:
            if not patient_id.isdigit():
                raise ValidationError({"patient": "Informe um ID numérico válido."})
            queryset = queryset.filter(patient_id=patient_id)
        return queryset

    def perform_create(self, serializer):
        patient = serializer.validated_data["patient"]
        self.require_assigned_patient(patient)
        serializer.save()


class CaregiverPatientViewSet(ReadOnlyModelViewSet):
    queryset = CaregiverPatient.objects.select_related("patient", "caregiver")
    serializer_class = CaregiverPatientSerializer

    def get_queryset(self):
        return self.queryset.filter(caregiver=self.request.user)


class DoseAdministrationViewSet(ModelViewSet):
    queryset = DoseAdministration.objects.select_related(
        "prescription__patient", "prescription__medicine", "caregiver"
    )
    serializer_class = DoseAdministrationSerializer
    http_method_names = ("get", "post", "head", "options")

    def get_queryset(self):
        queryset = self.queryset.filter(
            prescription__patient__caregiver__caregiver=self.request.user
        ).distinct()
        patient_id = self.request.query_params.get("patient")
        if patient_id:
            if not patient_id.isdigit():
                raise ValidationError({"patient": "Informe um ID numérico válido."})
            queryset = queryset.filter(prescription__patient_id=patient_id)
        scheduled_date = self.request.query_params.get("date")
        if scheduled_date:
            parsed_date = parse_date(scheduled_date)
            if parsed_date is None:
                raise ValidationError({"date": "Use o formato AAAA-MM-DD."})
            queryset = queryset.filter(scheduled_at__date=parsed_date)
        return queryset

    def perform_create(self, serializer):
        prescription = serializer.validated_data["prescription"]
        if not CaregiverPatient.objects.filter(
            patient=prescription.patient,
            caregiver=self.request.user,
        ).exists():
            raise PermissionDenied("O paciente não está vinculado a este cuidador.")
        serializer.save(status=DoseStatus.PENDING)

    @action(detail=True, methods=("post",))
    @transaction.atomic
    def mark(self, request, pk=None):
        dose = self.get_object()
        new_status = request.data.get("status")
        if new_status not in (DoseStatus.ADMINISTERED, DoseStatus.REFUSED):
            raise ValidationError(
                {"status": "Informe MINISTRADO ou RECUSADO."}
            )
        if dose.status != DoseStatus.PENDING:
            raise ValidationError({"status": "A dose já foi processada."})

        dose.status = new_status
        dose.caregiver = request.user
        dose.recorded_at = timezone.now()
        dose.save(update_fields=("status", "caregiver", "recorded_at"))

        if new_status == DoseStatus.ADMINISTERED:
            prescription = dose.prescription
            prescription.last_hour = dose.recorded_at.time()
            prescription.last_worker_gives_dosage = request.user
            prescription.save(
                update_fields=("last_hour", "last_worker_gives_dosage")
            )

        return Response(self.get_serializer(dose).data)


class ClinicalRecordViewSet(ModelViewSet):
    queryset = ClinicalRecord.objects.select_related("patient", "caregiver")
    serializer_class = ClinicalRecordSerializer
    http_method_names = ("get", "post", "head", "options")

    def get_queryset(self):
        queryset = self.queryset.filter(
            patient__caregiver__caregiver=self.request.user
        ).distinct()
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")
        parsed_from = parse_date(date_from) if date_from else None
        parsed_to = parse_date(date_to) if date_to else None
        if date_from and parsed_from is None:
            raise ValidationError({"date_from": "Use o formato AAAA-MM-DD."})
        if date_to and parsed_to is None:
            raise ValidationError({"date_to": "Use o formato AAAA-MM-DD."})
        if parsed_from and parsed_to and parsed_from > parsed_to:
            raise ValidationError(
                {"date_to": "A data final deve ser igual ou posterior à inicial."}
            )
        if parsed_from:
            queryset = queryset.filter(recorded_at__date__gte=parsed_from)
        if parsed_to:
            queryset = queryset.filter(recorded_at__date__lte=parsed_to)
        return queryset.order_by("recorded_at")

    def perform_create(self, serializer):
        patient = serializer.validated_data["patient"]
        if not CaregiverPatient.objects.filter(
            patient=patient,
            caregiver=self.request.user,
        ).exists():
            raise PermissionDenied("O paciente não está vinculado a este cuidador.")
        serializer.save(caregiver=self.request.user)
