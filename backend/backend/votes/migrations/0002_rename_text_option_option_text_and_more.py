# Generated by Django 5.0 on 2024-10-25 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='option',
            old_name='text',
            new_name='option_text',
        ),
        migrations.RemoveField(
            model_name='option',
            name='description',
        ),
    ]
