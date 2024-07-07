from django.urls import path
from .views import (
    IncomeCreateAPIView,
    IncomeListAPIView,
    IncomeDetailAPIView,
    IncomeUpdateDeleteAPIView,
    ExpenseCreateAPIView,
    ExpenseListAPIView,
    ExpenseDetailAPIView,
    ExpenseUpdateDeleteAPIView
)

urlpatterns = [
    #Main
    #path('<str:IDcommunity>/', ), #GET\ Dashboard 

    # Income URLs
    path('<str:IDcommunity>/incomes/', IncomeListAPIView.as_view(), name='income-list'),
    path('<str:IDcommunity>/incomes/create/', IncomeCreateAPIView.as_view(), name='income-create'),
    path('<str:IDcommunity>/incomes/<int:income_id>/', IncomeDetailAPIView.as_view(), name='income-detail'),
    path('<str:IDcommunity>/incomes/<int:income_id>/update-delete/', IncomeUpdateDeleteAPIView.as_view(), name='income-update-delete'),
    
    # Expense URLs
    path('<str:IDcommunity>/expenses/', ExpenseListAPIView.as_view(), name='expense-list'),
    path('<str:IDcommunity>/expenses/create/', ExpenseCreateAPIView.as_view(), name='expense-create'),
    path('<str:IDcommunity>/expenses/<int:expense_id>/', ExpenseDetailAPIView.as_view(), name='expense-detail'),
    path('<str:IDcommunity>/expenses/<int:expense_id>/update-delete/', ExpenseUpdateDeleteAPIView.as_view(), name='expense-update-delete'),
]
