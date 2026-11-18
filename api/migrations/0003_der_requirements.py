import datetime

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


def migrate_legacy_data(apps, schema_editor):
    database = schema_editor.connection.alias
    Patient = apps.get_model("api", "Patient")
    Responsible = apps.get_model("api", "Responsible")
    for patient in Patient.objects.using(database).all().iterator():
        responsible = Responsible.objects.using(database).get(
            pk=patient.responsible_id
        )
        if responsible.patient_id is None:
            responsible.patient_id = patient.pk
            responsible.emergency_contact = True
            responsible.save(
                update_fields=("patient", "emergency_contact")
            )
        else:
            values = {
                field: getattr(responsible, field)
                for field in (
                    "complete_name", "cpf", "rg", "birth_date", "email",
                    "main_cellphone", "secondary_cellphone",
                    "relationship_degree", "street", "number", "complement",
                    "neighborhood", "city", "state", "postal_code", "country",
                )
            }
            Responsible.objects.using(database).create(
                patient_id=patient.pk,
                emergency_contact=True,
                **values,
            )

    HospitalizationData = apps.get_model("api", "HospitalizationData")
    for hospitalization in HospitalizationData.objects.using(database).all().iterator():
        legacy_date = hospitalization.date or hospitalization.hour
        if legacy_date:
            hospitalization.admission_datetime = datetime.datetime.combine(
                legacy_date,
                datetime.time.min,
                tzinfo=datetime.timezone.utc,
            )
        else:
            hospitalization.admission_datetime = django.utils.timezone.now()
        hospitalization.save(update_fields=("admission_datetime",))

    CareGiver = apps.get_model("api", "CareGiver")
    from django.contrib.auth.hashers import identify_hasher, make_password

    for caregiver in CareGiver.objects.using(database).all().iterator():
        password = caregiver.password
        try:
            identify_hasher(password)
        except (ValueError, TypeError):
            password = make_password(password) if password else make_password(None)
        caregiver.password = password
        caregiver.save(update_fields=("password",))


def remove_duplicate_links(apps, schema_editor):
    database = schema_editor.connection.alias
    for model_name, fields in (
        ("CaregiverPatient", ("caregiver_id", "patient_id")),
        ("IllnessPatient", ("illness_id", "patient_id")),
    ):
        model = apps.get_model("api", model_name)
        seen = set()
        for item in model.objects.using(database).order_by("pk").iterator():
            key = tuple(getattr(item, field) for field in fields)
            if key in seen:
                item.delete(using=database)
            else:
                seen.add(key)


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0002_caregiver_password"),
    ]

    operations = [
        migrations.AddField(
            model_name="responsible",
            name="patient",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="responsibles",
                to="api.patient",
            ),
        ),
        migrations.AddField(
            model_name="responsible",
            name="relationship_degree",
            field=models.CharField(default="Não informado", max_length=50),
        ),
        migrations.AddField(
            model_name="responsible",
            name="emergency_contact",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="responsible",
            name="street",
            field=models.CharField(blank=True, default="", max_length=150),
        ),
        migrations.AddField(
            model_name="responsible",
            name="number",
            field=models.CharField(blank=True, default="", max_length=20),
        ),
        migrations.AddField(
            model_name="responsible",
            name="complement",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
        migrations.AddField(
            model_name="responsible",
            name="neighborhood",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
        migrations.AddField(
            model_name="responsible",
            name="city",
            field=models.CharField(blank=True, default="", max_length=100),
        ),
        migrations.AddField(
            model_name="responsible",
            name="state",
            field=models.CharField(blank=True, default="", max_length=2),
        ),
        migrations.AddField(
            model_name="responsible",
            name="postal_code",
            field=models.CharField(blank=True, default="", max_length=9),
        ),
        migrations.AddField(
            model_name="responsible",
            name="country",
            field=models.CharField(blank=True, default="", max_length=80),
        ),
        migrations.AddField(
            model_name="hospitalizationdata",
            name="admission_datetime",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="hospitalizationdata",
            name="discharge_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.RunPython(migrate_legacy_data, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="responsible",
            name="patient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="responsibles",
                to="api.patient",
            ),
        ),
        migrations.RemoveField(
            model_name="patient",
            name="responsible",
        ),
        migrations.AlterField(
            model_name="hospitalizationdata",
            name="admission_datetime",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.RemoveField(
            model_name="hospitalizationdata",
            name="date",
        ),
        migrations.RemoveField(
            model_name="hospitalizationdata",
            name="hour",
        ),
        migrations.AlterField(
            model_name="hospitalizationdata",
            name="room",
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name="hospitalizationdata",
            name="patient",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="hospitalization_data",
                to="api.patient",
            ),
        ),
        migrations.AlterField(
            model_name="hospitalizationdata",
            name="caregiver",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="api.caregiver",
            ),
        ),
        migrations.AlterField(
            model_name="allergies",
            name="type",
            field=models.CharField(
                choices=[
                    ("MEDICAMENTO", "Medicamento"),
                    ("ALIMENTAR", "Alimentar"),
                    ("OUTRA", "Outra"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="patient",
            name="cpf",
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name="patient",
            name="hip",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="patient",
                to="api.healthinsuranceplan",
            ),
        ),
        migrations.AlterField(
            model_name="patient",
            name="routine",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="patient",
                to="api.routine",
            ),
        ),
        migrations.AlterField(
            model_name="caregiver",
            name="cpf",
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name="caregiver",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="caregiver",
            name="password",
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name="patientmedicine",
            name="daily_frequency",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="patientmedicine",
            name="last_worker_gives_dosage",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="api.caregiver",
            ),
        ),
        migrations.AddField(
            model_name="routine",
            name="breakfast_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="routine",
            name="lunch_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="routine",
            name="dinner_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.RunPython(remove_duplicate_links, migrations.RunPython.noop),
        migrations.AddConstraint(
            model_name="caregiverpatient",
            constraint=models.UniqueConstraint(
                fields=("caregiver", "patient"),
                name="unique_caregiver_patient",
            ),
        ),
        migrations.AddConstraint(
            model_name="illnesspatient",
            constraint=models.UniqueConstraint(
                fields=("illness", "patient"),
                name="unique_patient_illness",
            ),
        ),
        migrations.CreateModel(
            name="DoseAdministration",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("scheduled_at", models.DateTimeField()),
                ("status", models.CharField(
                    choices=[
                        ("PENDENTE", "Pendente"),
                        ("MINISTRADO", "Ministrado"),
                        ("RECUSADO", "Recusado"),
                    ],
                    default="PENDENTE",
                    max_length=12,
                )),
                ("recorded_at", models.DateTimeField(blank=True, null=True)),
                ("caregiver", models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="dose_administrations",
                    to="api.caregiver",
                )),
                ("prescription", models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name="scheduled_doses",
                    to="api.patientmedicine",
                )),
            ],
            options={"ordering": ("scheduled_at",)},
        ),
        migrations.AddConstraint(
            model_name="doseadministration",
            constraint=models.UniqueConstraint(
                fields=("prescription", "scheduled_at"),
                name="unique_prescription_dose_time",
            ),
        ),
        migrations.CreateModel(
            name="ClinicalRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("description", models.TextField()),
                ("recorded_at", models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ("caregiver", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="clinical_records",
                    to="api.caregiver",
                )),
                ("patient", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="clinical_records",
                    to="api.patient",
                )),
            ],
            options={"ordering": ("recorded_at",)},
        ),
    ]
