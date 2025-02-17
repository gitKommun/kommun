from django.db import models
import uuid

class Supplier(models.Model):
    supplier_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"
        ordering = ["company_name"]

    def __str__(self):
        return f"{self.company_name} ({self.cif_nif})"