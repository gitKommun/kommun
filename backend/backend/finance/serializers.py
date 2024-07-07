from rest_framework import serializers
from .models import Income, Expense, Budget, Invoice

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        exclude = ('community',)

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        exclude = ('community',)

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        exclude = ('community',)

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        exclude = ('community',)