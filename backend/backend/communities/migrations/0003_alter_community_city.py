# Generated by Django 5.0.4 on 2025-01-20 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='city'),
        ),
    ]
