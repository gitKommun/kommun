# Generated by Django 5.0 on 2024-08-24 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_municipality_code_municipality_code_ine_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='municipality',
            name='code_ine_municipality',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='municipality',
            name='code_ine',
            field=models.CharField(max_length=5, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='municipality',
            name='postal_code',
            field=models.CharField(max_length=5),
        ),
    ]
