from django.db import models

class Province(models.Model):
    code = models.CharField(max_length=2, primary_key=True) #postal code 2 first digits = INE
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Municipality(models.Model):
    code_ine = models.CharField(max_length=5, primary_key=True)
    name = models.CharField(max_length=100)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='municipalities')

    def __str__(self):
        return f"{self.name}"
    
class PostalCode(models.Model):
    postal_code = models.CharField(max_length=5)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='postal_codes')

    def __str__(self):
        return self.postal_code
