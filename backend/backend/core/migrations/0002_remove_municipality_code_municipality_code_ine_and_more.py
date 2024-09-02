# Generated by Django 5.0 on 2024-08-24 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='municipality',
            name='code',
        ),
        migrations.AddField(
            model_name='municipality',
            name='code_ine',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='municipality',
            name='postal_code',
            field=models.CharField(default=1, max_length=5, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='province',
            name='code',
            field=models.CharField(max_length=2, primary_key=True, serialize=False),
        ),
    ]
