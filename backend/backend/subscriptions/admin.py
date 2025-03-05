from django.contrib import admin
from .models import Plan, Subscription

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name',)
    list_filter = ('price',)
    ordering = ('price',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('community', 'plan', 'start_date', 'end_date')
    search_fields = ('community__name', 'plan__name')
    list_filter = ('plan',)
    ordering = ('-start_date',)

