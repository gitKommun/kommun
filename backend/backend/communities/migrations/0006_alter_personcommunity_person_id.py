# Generated by Django 5.0 on 2024-07-17 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0005_alter_personcommunity_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personcommunity',
            name='person_id',
            field=models.PositiveIntegerField(),
        ),
    ]
