# Generated by Django 5.0.4 on 2024-10-28 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommonArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_id', models.PositiveIntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('type', models.CharField(blank=True, max_length=50, null=True, verbose_name='type')),
                ('reservable', models.BooleanField(default=False, verbose_name='reservable')),
                ('reservation_duration', models.PositiveIntegerField(blank=True, null=True, verbose_name='reservation duration')),
                ('time_unit', models.CharField(blank=True, choices=[('MIN', 'Minutes'), ('HOUR', 'Hours'), ('DAY', 'Days')], max_length=4, null=True, verbose_name='time unit')),
            ],
            options={
                'verbose_name': 'Common Area',
                'verbose_name_plural': 'Common Areas',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_id', models.PositiveIntegerField(blank=True, null=True)),
                ('start_time', models.DateTimeField(verbose_name='start time')),
                ('end_time', models.DateTimeField(verbose_name='end time')),
                ('duration', models.PositiveIntegerField(verbose_name='duration')),
                ('time_unit', models.CharField(choices=[('MIN', 'Minutes'), ('HOUR', 'Hours'), ('DAY', 'Days')], max_length=4, verbose_name='time unit')),
            ],
            options={
                'verbose_name': 'Reservation',
                'verbose_name_plural': 'Reservations',
                'ordering': ['start_time'],
            },
        ),
    ]
