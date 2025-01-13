# Generated by Django 5.0.4 on 2024-10-28 18:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='description')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='amount')),
                ('currency', models.CharField(default='EUR', max_length=3, verbose_name='currency')),
                ('date_received', models.DateField(verbose_name='date received')),
                ('type', models.CharField(choices=[('periodic_fee', 'Periodic Fee'), ('extraordinary_fee', 'Extraordinary Fee'), ('other', 'Other')], max_length=20, verbose_name='income type')),
            ],
            options={
                'verbose_name': 'Income',
                'verbose_name_plural': 'Incomes',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=50, unique=True, verbose_name='invoice number')),
                ('date_issued', models.DateField(verbose_name='date issued')),
                ('due_date', models.DateField(verbose_name='due date')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='amount')),
                ('currency', models.CharField(default='EUR', max_length=3, verbose_name='currency')),
                ('is_paid', models.BooleanField(default=False, verbose_name='is paid')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(verbose_name='year')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='total_amount')),
                ('currency', models.CharField(default='EUR', max_length=3, verbose_name='currency')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to='communities.community')),
            ],
            options={
                'verbose_name': 'Budget',
                'verbose_name_plural': 'Budgets',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='description')),
                ('paid_to', models.CharField(max_length=255, verbose_name='description')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='amount')),
                ('currency', models.CharField(default='EUR', max_length=3, verbose_name='currency')),
                ('date_incurred', models.DateField(verbose_name='date incurred')),
                ('category', models.CharField(choices=[('electricity', 'Electricity'), ('water', 'Water'), ('general_maintenance', 'General Maintenance'), ('repairs', 'Repairs'), ('elevator', 'Elevator'), ('pool', 'Pool'), ('administrator', 'Administrator'), ('taxes', 'Taxes'), ('other', 'Other')], max_length=20, verbose_name='category')),
                ('community', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to='communities.community')),
            ],
            options={
                'verbose_name': 'Expense',
                'verbose_name_plural': 'Expenses',
            },
        ),
    ]
