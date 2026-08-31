from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets

from api.models import Patient

class PatientViewset(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by("name")
    filter_backends = (DjangoFilterBackend,)

    
