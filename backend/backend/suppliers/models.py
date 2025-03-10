from django.db import models
import uuid
from claims.models import Claim, Community
from members.models import User
from django.db.models import Max
from datetime import datetime
import random
import string

class Supplier(models.Model):
    supplier_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier_number = models.CharField(max_length=20, unique=True, editable=False)  # Formato: SUP-0001
    company_name = models.CharField(max_length=255, verbose_name="Company Name")
    cif_nif = models.CharField(max_length=20, unique=True, verbose_name="CIF/NIF")
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    email = models.EmailField(unique=True, verbose_name="Email")
    address = models.TextField(verbose_name="Address")
    type = models.CharField(max_length=50, verbose_name="Type of Service")
    rating = models.PositiveIntegerField(default=0, verbose_name="Rating (1-5)")
    reviews = models.PositiveIntegerField(default=0, verbose_name="Number of Reviews")
    contact_person = models.CharField(max_length=255, verbose_name="Contact Person")
    contact_person_email = models.EmailField(verbose_name="Contact Person Email")
    contact_person_phone = models.CharField(max_length=20, verbose_name="Contact Person Phone")
    additional_info = models.TextField(null=True, blank=True, verbose_name="Additional Information")

    def generate_supplier_number(self):
        # Generar componente aleatorio (6 caracteres alfanuméricos)
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
        # Formato: SUP-ABCD12
        return f'SUP-{random_chars}'

    def save(self, *args, **kwargs):
        if not self.supplier_number:
            while True:
                new_number = self.generate_supplier_number()
                if not Supplier.objects.filter(supplier_number=new_number).exists():
                    self.supplier_number = new_number
                    break
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.supplier_number} - {self.company_name}"

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        ordering = ["company_name"]

class WorkOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En Progreso'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
        ('rejected', 'Rechazada'),
    ]

    work_order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relaciones
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='work_orders')
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE, related_name='work_orders', null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='work_orders')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_work_orders')

    def save(self, *args, **kwargs):
        if not self.order_number:
            year = datetime.now().year
            # Obtener el último número de orden para esta comunidad y año
            last_order = WorkOrder.objects.filter(
                community=self.community,
                order_number__startswith=f'WO-{self.community.community_id}-{year}'
            ).aggregate(Max('order_number'))['order_number__max']
            
            if last_order:
                # Extraer el número y aumentarlo en 1
                last_number = int(last_order.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            # Crear el nuevo número de orden incluyendo el ID de la comunidad
            self.order_number = f'WO-{self.community.community_id}-{year}-{new_number:04d}'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} - {self.title}"

    class Meta:
        ordering = ['-created_at']
        # Asegurar que el order_number es único por comunidad
        unique_together = ['community', 'order_number']

class WorkOrderSupplierRequest(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Enviada'),
        ('seen', 'Vista'),
        ('accepted', 'Aceptada'),
        ('rejected', 'Rechazada'),
        ('expired', 'Expirada'),
        ('cancelled', 'Cancelada'),
        ('completed', 'Completada'),
    ]

    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='supplier_requests')
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, related_name='work_order_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='sent')
    sent_at = models.DateTimeField(auto_now_add=True)
    response_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)  # Fecha límite para responder

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.work_order.order_number} - {self.supplier.company_name} - {self.get_status_display()}"
    

