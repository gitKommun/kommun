from django.contrib import admin
from .models import Supplier, WorkOrder, WorkOrderSupplierRequest

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_number', 'company_name', 'cif_nif', 'type', 'rating', 'contact_person', 'phone')
    list_filter = ('type', 'rating')
    search_fields = ('supplier_number', 'company_name', 'cif_nif', 'contact_person', 'email')
    ordering = ('supplier_number',)
    fieldsets = (
        ('Información Principal', {
            'fields': ('supplier_id', 'supplier_number', 'company_name', 'cif_nif', 'type')
        }),
        ('Contacto', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Valoración', {
            'fields': ('rating', 'reviews')
        }),
        ('Persona de Contacto', {
            'fields': ('contact_person', 'contact_person_email', 'contact_person_phone')
        }),
        ('Información Adicional', {
            'fields': ('additional_info',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('supplier_id', 'supplier_number')

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'title', 'community', 'supplier', 'status', 'created_at')
    list_filter = ('status', 'community', 'supplier')
    search_fields = ('order_number', 'title', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('work_order_id', 'order_number', 'created_at', 'updated_at')
    fieldsets = (
        ('Información Principal', {
            'fields': ('work_order_id', 'order_number', 'title', 'description')
        }),
        ('Estado y Fechas', {
            'fields': ('status', 'start_date', 'end_date', 'created_at', 'updated_at')
        }),
        ('Relaciones', {
            'fields': ('community', 'claim', 'supplier', 'created_by')
        }),
    )

@admin.register(WorkOrderSupplierRequest)
class WorkOrderSupplierRequestAdmin(admin.ModelAdmin):
    list_display = ('work_order', 'supplier', 'status', 'sent_at', 'response_at', 'expires_at')
    list_filter = ('status', 'supplier')
    search_fields = ('work_order__order_number', 'supplier__company_name')
    ordering = ('-sent_at',)
    readonly_fields = ('request_id', 'sent_at', 'response_at')
    fieldsets = (
        ('Información Principal', {
            'fields': ('request_id', 'work_order', 'supplier')
        }),
        ('Estado y Respuesta', {
            'fields': ('status', 'rejection_reason', 'notes')
        }),
        ('Fechas', {
            'fields': ('sent_at', 'response_at', 'expires_at')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('work_order', 'supplier')
        return self.readonly_fields
