# Generated by Django 5.0 on 2024-06-24 18:22

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('surnames', models.CharField(max_length=150, verbose_name='surnames')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='Birthdate')),
                ('addressLetters', models.CharField(max_length=255, verbose_name='postal address')),
                ('phoneNumber', models.CharField(blank=True, max_length=20, null=True, verbose_name='phone number')),
                ('bankAccount', models.CharField(blank=True, max_length=22, null=True, verbose_name='bank account')),
                ('languageConf', models.CharField(blank=True, choices=[('EN', 'English'), ('ES', 'Spanish')], max_length=2, null=True, verbose_name='language configuration')),
                ('documentID', models.CharField(blank=True, max_length=20, null=True, verbose_name='user ID')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('companyName', models.CharField(blank=True, max_length=20, null=True, verbose_name='company name')),
                ('numCollegiate', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='number collegiate')),
            ],
            options={
                'verbose_name': 'Administrator',
                'verbose_name_plural': 'Administrators',
            },
            bases=('members.user',),
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('hasPendingPayment', models.BooleanField(blank=True, null=True)),
                ('properties', models.ManyToManyField(blank=True, related_name='owners', to='communities.property', verbose_name='Properties')),
            ],
            options={
                'verbose_name': 'Owner',
                'verbose_name_plural': 'Owners',
            },
            bases=('members.user',),
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('properties', models.ManyToManyField(blank=True, related_name='tenants', to='communities.property', verbose_name='Properties')),
            ],
            options={
                'verbose_name': 'Tenant',
                'verbose_name_plural': 'Tenants',
            },
            bases=('members.user',),
        ),
    ]
