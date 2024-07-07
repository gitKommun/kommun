from django.db import models
from django.utils.translation import gettext_lazy as _
from members.models import User
from communities.models import Community

class Budget(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='budgets')
    year = models.PositiveIntegerField(_('year'))
    total_amount =  models.DecimalField(_('total_amount'), max_digits=10, decimal_places=2)
    currency = models.CharField(_('currency'), max_length=3, default='EUR')

    class Meta:
        unique_together = ('community', 'year')
        verbose_name = _('Budget')
        verbose_name_plural = _('Budgets')

    def __str__(self):
        return f"Budget for {self.community.nameCommunity} - {self.year}"

class Income(models.Model):
    class IncomeType(models.TextChoices):
        PERIODIC_FEE = 'periodic_fee', _('Periodic Fee')
        EXTRAORDINARY_FEE = 'extraordinary_fee', _('Extraordinary Fee')
        OTHER = 'other', _('Other')

    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='incomes')
    description = models.CharField(_('description'), max_length=255, null=True, blank=True)
    amount = models.DecimalField(_('amount'), max_digits=6, decimal_places=2)
    currency = models.CharField(_('currency'), max_length=3, default='EUR')
    date_received = models.DateField(_('date received'))
    type = models.CharField(_('income type'), max_length=20, choices=IncomeType.choices)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_incomes')
    paid_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='paid_incomes')

    class Meta:
        verbose_name = _('Income')
        verbose_name_plural = _('Incomes')

    def __str__(self):
        return f"Income for {self.community.nameCommunity} on {self.date_received}"


class Expense(models.Model):
    class ExpenseCategory(models.TextChoices):
        ELECTRICITY = 'electricity', _('Electricity')
        WATER = 'water', _('Water')
        GENERAL_MAINTENANCE = 'general_maintenance', _('General Maintenance')
        REPAIRS = 'repairs', _('Repairs')
        ELEVATOR = 'elevator', _('Elevator')
        POOL = 'pool', _('Pool')
        ADMINISTRATOR = 'administrator', _('Administrator')
        TAXES = 'taxes', _('Taxes')
        OTHER = 'other', _('Other')

    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='expenses')
    description = models.CharField(_('description'), max_length=255)
    paid_to = models.CharField(_('description'), max_length=255)
    amount = models.DecimalField(_('amount'), max_digits=6, decimal_places=2)
    currency = models.CharField(_('currency'), max_length=3, default='EUR')
    date_incurred = models.DateField(_('date incurred'))
    category = models.CharField(_('category'), max_length=20, choices=ExpenseCategory.choices)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_expenses')

    class Meta:
        verbose_name = _('Expense')
        verbose_name_plural = _('Expenses')

    def __str__(self):
        return f"Expense for {self.community.nameCommunity} on {self.date_incurred}"


class Invoice(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='invoices')
    number = models.CharField(_('invoice number'), max_length=50, unique=True)
    date_issued = models.DateField(_('date issued'))
    due_date = models.DateField(_('due date'))
    amount = models.DecimalField(_('amount'), max_digits=6, decimal_places=2)
    currency = models.CharField(_('currency'), max_length=3, default='EUR')
    is_paid = models.BooleanField(_('is paid'), default=False)
    expense = models.ForeignKey('finance.Expense', on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')

    class Meta:
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')

    def __str__(self):
        return f"Invoice {self.number} for {self.community.nameCommunity}"
    
