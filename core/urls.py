"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.viewsets.caregiver_viewset import CareGiverViewSet
from api.viewsets.patient_viewset import PatientViewSet
from api.auth_views import (
    LoginView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
)
from api.viewsets.supporting_viewsets import (
    AllergyViewSet,
    CaregiverPatientViewSet,
    ClinicalRecordViewSet,
    DoseAdministrationViewSet,
    HealthInsurancePlanViewSet,
    HospitalizationDataViewSet,
    IllnessPatientViewSet,
    IllnessViewSet,
    MedicineViewSet,
    PatientMedicineViewSet,
    ResponsibleViewSet,
    RoutineViewSet,
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'caregivers', CareGiverViewSet, basename='caregiver')
router.register(r'responsibles', ResponsibleViewSet, basename='responsible')
router.register(r'hospitalizations', HospitalizationDataViewSet, basename='hospitalization')
router.register(r'allergies', AllergyViewSet, basename='allergy')
router.register(r'insurance-plans', HealthInsurancePlanViewSet, basename='insurance-plan')
router.register(r'routines', RoutineViewSet, basename='routine')
router.register(r'illnesses', IllnessViewSet, basename='illness')
router.register(r'patient-illnesses', IllnessPatientViewSet, basename='patient-illness')
router.register(r'medicines', MedicineViewSet, basename='medicine')
router.register(r'prescriptions', PatientMedicineViewSet, basename='prescription')
router.register(r'caregiver-patients', CaregiverPatientViewSet, basename='caregiver-patient')
router.register(r'doses', DoseAdministrationViewSet, basename='dose')
router.register(r'clinical-records', ClinicalRecordViewSet, basename='clinical-record')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('api/auth/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('api/', include(router.urls)),
]
