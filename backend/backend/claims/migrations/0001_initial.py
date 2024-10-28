# Generated by Django 5.0.4 on 2024-10-23 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('maintenance', 'Maintenance'), ('cleaning', 'Cleaning'), ('security', 'Security')], max_length=50)),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')], default='information', max_length=20)),
                ('status', models.CharField(choices=[('reported', 'Reported'), ('in_process', 'In Process'), ('resolved', 'Resolved'), ('closed', 'Closed')], default='reported', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('incident_date', models.DateTimeField(blank=True, null=True)),
                ('problem_persists', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClaimComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClaimStatusRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('reported', 'Reported'), ('in_process', 'In Process'), ('resolved', 'Resolved'), ('closed', 'Closed')], max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
