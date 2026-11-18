from django.contrib.auth.hashers import check_password
from django.core import mail
from django.test import TestCase, override_settings
from django.utils import timezone
from rest_framework.test import APIClient
from urllib.parse import parse_qs, urlparse

from api.models import (
    CareGiver,
    HospitalizationData,
    HealthInsurancePlan,
    Medicine,
    Patient,
    PatientMedicine,
    Routine,
)


class ApiTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        registration = self.client.post(
            '/api/caregivers/',
            {
                'complete_name': 'Ana Silva',
                'cpf': '12345678901',
                'email': 'ana@example.com',
                'shift_start_time': '08:00:00',
                'shift_end_time': '18:00:00',
                'pause_time': '12:00:00',
                'cellphone': '11999999999',
                'password': 'StrongPass123',
            },
            format='json',
        )
        self.assertEqual(registration.status_code, 201, registration.data)
        login = self.client.post(
            '/api/auth/login/',
            {'email': 'ana@example.com', 'password': 'StrongPass123'},
            format='json',
        )
        self.assertEqual(login.status_code, 200, login.data)
        self.token = login.data['token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        self.caregiver = CareGiver.objects.get(email='ana@example.com')

    def create_patient(self):
        routine = Routine.objects.create(
            sleep_time='22:00:00',
            wakeup_time='06:00:00',
            bath_time='07:00:00',
        )
        plan = HealthInsurancePlan.objects.create(
            health_insurance_plan_name='Plano',
            membership_card_number='PLANO-123',
            expiration_date='2030-12-31',
        )
        payload = {
            'complete_name': 'Joao Silva',
            'birth_date': '2015-05-10',
            'main_diagnosis': 'Diagnostico',
            'religion': 'Catolica',
            'cpf': '11122233344',
            'rg': '987654321',
            'genre': 1,
            'continuous_use_medicines': 'Nenhum',
            'blood_type': 7,
            'routine': routine.pk,
            'hip': plan.pk,
            'temperament': 'Calmo',
            'hobbies': 'Musica',
            'secondary_health_problems': 'Nenhum',
            'responsibles': [{
                'complete_name': 'Maria Silva',
                'cpf': '98765432100',
                'rg': '123456789',
                'birth_date': '1980-01-01',
                'email': 'maria@example.com',
                'main_cellphone': '11988888888',
                'relationship_degree': 'Mae',
                'emergency_contact': True,
                'street': 'Rua A',
                'number': '10',
                'complement': '',
                'neighborhood': 'Centro',
                'city': 'Sao Paulo',
                'state': 'SP',
                'postal_code': '01000-000',
                'country': 'Brasil',
            }],
            'admission': {
                'room': '101',
                'main_diagnosis': 'Diagnostico de admissao',
            },
        }
        response = self.client.post('/api/patients/', payload, format='json')
        self.assertEqual(response.status_code, 201, response.data)
        return Patient.objects.get(pk=response.data['id'])


class AuthenticationAndCaregiverTests(ApiTestCase):
    def test_password_is_hashed_and_login_required(self):
        self.assertTrue(check_password('StrongPass123', self.caregiver.password))
        self.assertNotEqual(self.caregiver.password, 'StrongPass123')

        unauthenticated = APIClient().get('/api/patients/')
        self.assertEqual(unauthenticated.status_code, 401)

        invalid_login = APIClient().post(
            '/api/auth/login/',
            {'email': 'ana@example.com', 'password': 'wrong-password'},
            format='json',
        )
        self.assertEqual(invalid_login.status_code, 401)

    def test_formatted_duplicate_cpf_is_rejected(self):
        response = APIClient().post(
            '/api/caregivers/',
            {
                'complete_name': 'Ana Silva Duplicada',
                'cpf': '123.456.789-01',
                'email': 'ana2@example.com',
                'shift_start_time': '08:00:00',
                'shift_end_time': '18:00:00',
                'pause_time': '12:00:00',
                'cellphone': '11999999997',
                'password': 'AnotherPass123',
            },
            format='json',
        )
        self.assertEqual(response.status_code, 400)

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_password_reset_uses_one_time_token(self):
        response = APIClient().post(
            '/api/auth/password-reset/',
            {'email': self.caregiver.email},
            format='json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        reset_url = mail.outbox[0].body.split(': ', maxsplit=1)[1]
        reset_token = parse_qs(urlparse(reset_url).query)['token'][0]

        reset = APIClient().post(
            '/api/auth/password-reset/confirm/',
            {
                'email': self.caregiver.email,
                'token': reset_token,
                'password': 'UpdatedPass123',
            },
            format='json',
        )
        self.assertEqual(reset.status_code, 200, reset.data)
        self.caregiver.refresh_from_db()
        self.assertTrue(check_password('UpdatedPass123', self.caregiver.password))

        second_use = APIClient().post(
            '/api/auth/password-reset/confirm/',
            {
                'email': self.caregiver.email,
                'token': reset_token,
                'password': 'OtherPass123',
            },
            format='json',
        )
        self.assertEqual(second_use.status_code, 400)


class PatientAndClinicalWorkflowTests(ApiTestCase):
    def test_patient_create_search_update_and_forbidden_delete(self):
        patient = self.create_patient()
        detail = self.client.get(f'/api/patients/{patient.pk}/')
        self.assertEqual(detail.status_code, 200)
        self.assertTrue(detail.data['active'])
        self.assertEqual(len(detail.data['responsibles']), 1)

        search = self.client.get('/api/patients/?name=joao')
        self.assertEqual(search.status_code, 200)
        self.assertEqual(len(search.data), 1)

        update = self.client.patch(
            f'/api/patients/{patient.pk}/',
            {'complete_name': 'Joao Souza'},
            format='json',
        )
        self.assertEqual(update.status_code, 200)
        self.assertEqual(update.data['complete_name'], 'Joao Souza')

        delete = self.client.delete(f'/api/patients/{patient.pk}/')
        self.assertEqual(delete.status_code, 405)
        self.assertTrue(Patient.objects.filter(pk=patient.pk).exists())

        hospitalization = HospitalizationData.objects.get(patient=patient)
        discharge = self.client.patch(
            f'/api/hospitalizations/{hospitalization.pk}/',
            {'discharge_date': timezone.localdate().isoformat()},
            format='json',
        )
        self.assertEqual(discharge.status_code, 200, discharge.data)
        detail = self.client.get(f'/api/patients/{patient.pk}/')
        self.assertFalse(detail.data['active'])

    def test_caregiver_cannot_act_on_unassigned_patient(self):
        patient = self.create_patient()
        registration = APIClient().post(
            '/api/caregivers/',
            {
                'complete_name': 'Bruno Silva',
                'cpf': '12345678902',
                'email': 'bruno@example.com',
                'shift_start_time': '08:00:00',
                'shift_end_time': '18:00:00',
                'pause_time': '12:00:00',
                'cellphone': '11999999998',
                'password': 'AnotherPass123',
            },
            format='json',
        )
        self.assertEqual(registration.status_code, 201, registration.data)
        other_client = APIClient()
        login = other_client.post(
            '/api/auth/login/',
            {'email': 'bruno@example.com', 'password': 'AnotherPass123'},
            format='json',
        )
        other_client.credentials(
            HTTP_AUTHORIZATION=f"Token {login.data['token']}"
        )
        self.assertEqual(other_client.get('/api/patients/').data, [])
        denied = other_client.post(
            '/api/clinical-records/',
            {'patient': patient.pk, 'description': 'Sem vínculo'},
            format='json',
        )
        self.assertEqual(denied.status_code, 403)

    def test_clinical_record_is_audited_and_date_filterable(self):
        patient = self.create_patient()
        create = self.client.post(
            '/api/clinical-records/',
            {'patient': patient.pk, 'description': 'Paciente descansou bem.'},
            format='json',
        )
        self.assertEqual(create.status_code, 201, create.data)
        self.assertEqual(create.data['caregiver'], self.caregiver.pk)
        self.assertIsNotNone(create.data['recorded_at'])
        edit = self.client.patch(
            f"/api/clinical-records/{create.data['id']}/",
            {'description': 'Editado'},
            format='json',
        )
        self.assertEqual(edit.status_code, 405)

        today = timezone.localdate().isoformat()
        mural = self.client.get(
            f'/api/clinical-records/?date_from={today}&date_to={today}'
        )
        self.assertEqual(mural.status_code, 200)
        self.assertEqual(len(mural.data), 1)

    def test_dose_starts_pending_and_only_mark_endpoint_records_actor(self):
        patient = self.create_patient()
        medicine = Medicine.objects.create(medicine_name='Medicamento')
        prescription = PatientMedicine.objects.create(
            patient=patient,
            medicine=medicine,
            dosage='1',
            daily_frequency='08:00',
            start_date='2026-01-01',
            end_date='2027-01-01',
        )
        scheduled_at = timezone.now().isoformat()
        create = self.client.post(
            '/api/doses/',
            {'prescription': prescription.pk, 'scheduled_at': scheduled_at},
            format='json',
        )
        self.assertEqual(create.status_code, 201, create.data)
        self.assertEqual(create.data['status'], 'PENDENTE')
        self.assertIsNone(create.data['caregiver'])
        today = timezone.localdate().isoformat()
        scheduled_today = self.client.get(f'/api/doses/?date={today}')
        self.assertEqual(scheduled_today.status_code, 200)
        self.assertEqual(len(scheduled_today.data), 1)

        mark = self.client.post(
            f"/api/doses/{create.data['id']}/mark/",
            {'status': 'MINISTRADO'},
            format='json',
        )
        self.assertEqual(mark.status_code, 200, mark.data)
        self.assertEqual(mark.data['status'], 'MINISTRADO')
        self.assertEqual(mark.data['caregiver'], self.caregiver.pk)
        self.assertIsNotNone(mark.data['recorded_at'])

        prescription.refresh_from_db()
        self.assertEqual(
            prescription.last_worker_gives_dosage_id,
            self.caregiver.pk,
        )

        duplicate_mark = self.client.post(
            f"/api/doses/{create.data['id']}/mark/",
            {'status': 'RECUSADO'},
            format='json',
        )
        self.assertEqual(duplicate_mark.status_code, 400)
