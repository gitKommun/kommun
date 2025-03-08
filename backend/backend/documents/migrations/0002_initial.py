# Generated by Django 5.0 on 2025-02-28 16:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('communities', '0002_initial'),
        ('documents', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='upload_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='folder',
            name='community',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='communities.community'),
        ),
        migrations.AlterUniqueTogether(
            name='document',
            unique_together={('community', 'document_id')},
        ),
        migrations.AlterUniqueTogether(
            name='folder',
            unique_together={('community', 'folder_id')},
        ),
    ]
