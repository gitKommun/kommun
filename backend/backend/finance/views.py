from rest_framework import generics
from .models import Income, Expense, Budget
from .serializers import IncomeSerializer, ExpenseSerializer, BudgetSerializer

# Income Views
class IncomeCreateAPIView(generics.CreateAPIView):
    serializer_class = IncomeSerializer

    def perform_create(self, serializer):
        serializer.save(community_id=self.kwargs['IDcommunity'], created_by=self.request.user)

class IncomeListAPIView(generics.ListAPIView):
    serializer_class = IncomeSerializer

    def get_queryset(self):
        return Income.objects.filter(community_id=self.kwargs['IDcommunity'])

class IncomeDetailAPIView(generics.RetrieveAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    lookup_url_kwarg = 'income_id'

    def get_queryset(self):
        return Income.objects.filter(community_id=self.kwargs['IDcommunity'])

class IncomeUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    lookup_url_kwarg = 'income_id'

    def get_queryset(self):
        return Income.objects.filter(community_id=self.kwargs['IDcommunity'])


# Expense Views
class ExpenseCreateAPIView(generics.CreateAPIView):
    serializer_class = ExpenseSerializer

    def perform_create(self, serializer):
        serializer.save(community_id=self.kwargs['IDcommunity'], created_by=self.request.user)

class ExpenseListAPIView(generics.ListAPIView):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(community_id=self.kwargs['IDcommunity'])

class ExpenseDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    lookup_url_kwarg = 'expense_id'

    def get_queryset(self):
        return Expense.objects.filter(community_id=self.kwargs['IDcommunity'])

class ExpenseUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    lookup_url_kwarg = 'expense_id'

    def get_queryset(self):
        return Expense.objects.filter(community_id=self.kwargs['IDcommunity'])
