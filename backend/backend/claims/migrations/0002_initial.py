# Generated by Django 5.0 on 2024-08-23 14:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('claims', '0001_initial'),
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='community',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='claims', to='communities.community'),
        ),
    ]
