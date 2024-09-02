# Generated by Django 5.0 on 2024-08-24 18:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_municipality_code_ine_municipality_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='municipality',
            name='code_ine_municipality',
        ),
        migrations.RemoveField(
            model_name='municipality',
            name='postal_code',
        ),
        migrations.CreateModel(
            name='PostalCode',
            fields=[
                ('postal_code', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postal_codes', to='core.municipality')),
            ],
        ),
    ]
