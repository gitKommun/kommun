# Generated by Django 5.0.4 on 2024-10-23 07:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_id', models.PositiveIntegerField()),
                ('surface_area', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='surface area')),
                ('participation_coefficient', models.DecimalField(blank=True, decimal_places=4, max_digits=5, null=True, verbose_name='participation coefficient')),
                ('usage', models.CharField(blank=True, choices=[('COMERCIAL', 'Comercial'), ('ALMACEN-ESTACIONAMIENTO', 'Almacén-Estacionamiento'), ('RESIDENCIAL', 'Residencial'), ('INDUSTRIAL', 'Industrial')], max_length=50, null=True)),
                ('address_complete', models.CharField(blank=True, max_length=200, null=True, verbose_name='address')),
                ('block', models.CharField(blank=True, max_length=50, null=True, verbose_name='block')),
                ('staircase', models.CharField(blank=True, max_length=50, null=True, verbose_name='staircase')),
                ('floor', models.CharField(blank=True, max_length=50, null=True, verbose_name='floor')),
                ('door', models.CharField(blank=True, max_length=50, null=True, verbose_name='door')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='communities.community')),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Properties',
                'ordering': ['community', 'property_id'],
                'unique_together': {('community', 'property_id')},
            },
        ),
        migrations.CreateModel(
            name='PropertyRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('owner', 'Owner'), ('tenant', 'Tenant')], default='owner', max_length=10)),
                ('community', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='properties_person_relationships', to='communities.community')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_relationships', to='communities.personcommunity')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationships', to='properties.property')),
            ],
            options={
                'unique_together': {('community', 'property', 'person', 'type')},
            },
        ),
    ]
