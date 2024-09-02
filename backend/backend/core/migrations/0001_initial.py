# Generated by Django 5.0 on 2024-08-23 14:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('code', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('code', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('province', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='municipalities', to='core.province')),
            ],
        ),
    ]
