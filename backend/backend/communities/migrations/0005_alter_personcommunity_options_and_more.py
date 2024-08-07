# Generated by Django 5.0 on 2024-07-17 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0004_alter_propertyrelationship_person'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='personcommunity',
            options={'ordering': ['community', 'person_id']},
        ),
        migrations.AddField(
            model_name='personcommunity',
            name='person_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='personcommunity',
            unique_together={('community', 'person_id')},
        ),
    ]
