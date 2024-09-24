# Generated by Django 5.0 on 2024-09-19 17:33

import communities.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonCommunity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.PositiveIntegerField()),
                ('user_status', models.CharField(choices=[('active', 'Activo'), ('disabled', 'Deshabilitado'), ('temp', 'Temporal'), ('not_registered', 'No registrado')], default='active', max_length=14)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='email address')),
                ('name', models.CharField(blank=True, max_length=30, null=True, verbose_name='name')),
                ('surnames', models.CharField(max_length=120, verbose_name='surnames')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='Birthdate')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='postal address')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='phone number')),
                ('personal_id_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='user ID')),
                ('personal_id_type', models.CharField(blank=True, choices=[('DNI', 'DNI'), ('NIE', 'NIE'), ('PASSPORT', 'Passport')], max_length=20, null=True, verbose_name='document type')),
            ],
            options={
                'ordering': ['community'],
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Community',
            fields=[
                ('community_id', models.CharField(default=communities.models.generate_idcommunity_default, max_length=12, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(default='Mi comunidad', max_length=40, verbose_name='community name')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='address')),
                ('postal_code', models.CharField(blank=True, max_length=12, null=True, verbose_name='postal code')),
                ('cif', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='community nif')),
                ('catastral_ref', models.CharField(blank=True, max_length=50, null=True, verbose_name='catastral reference')),
                ('configuration_is_completed', models.BooleanField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=communities.models.document_path)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='communities', to='core.municipality')),
            ],
            options={
                'verbose_name': 'Community',
                'verbose_name_plural': 'Communities',
            },
        ),
    ]
