# Generated by Django 5.0.4 on 2024-10-28 18:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('communities', '0001_initial'),
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='main_contact_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='communities_main', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='community',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='communities', to='core.province'),
        ),
        migrations.AddField(
            model_name='personcommunity',
            name='community',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='people', to='communities.community'),
        ),
        migrations.AddField(
            model_name='personcommunity',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profiles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='personcommunity',
            name='roles',
            field=models.ManyToManyField(blank=True, null=True, to='communities.role'),
        ),
        migrations.AlterUniqueTogether(
            name='personcommunity',
            unique_together={('community', 'person_id')},
        ),
    ]
