# Generated by Django 5.0 on 2024-07-17 18:19

import django.core.validators
import documents.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_alter_document_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to=documents.models.document_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'txt', 'doc', 'docx', 'jpeg', 'jpg', 'png', 'xls', 'xlsx', 'csv'])]),
        ),
    ]
