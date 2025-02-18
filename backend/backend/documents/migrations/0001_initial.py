# Generated by Django 5.0.4 on 2025-02-17 15:04

import django.core.validators
import django.db.models.deletion
import documents.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('folder_id', models.PositiveIntegerField()),
                ('parent_folder_id', models.PositiveIntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'ordering': ['community', 'folder_id'],
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to=documents.models.document_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'txt', 'doc', 'docx', 'jpeg', 'jpg', 'png', 'xls', 'xlsx', 'csv'])])),
                ('folder_id', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('document_id', models.PositiveIntegerField()),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='communities.community')),
            ],
            options={
                'ordering': ['community', 'document_id'],
            },
        ),
    ]
