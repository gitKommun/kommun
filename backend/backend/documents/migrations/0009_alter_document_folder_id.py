# Generated by Django 5.0 on 2024-07-21 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0008_folder_parent_folder_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='folder_id',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
