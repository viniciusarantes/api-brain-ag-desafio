from django.db import models

from rural.utils import STATE_CHOICES


class Producer(models.Model):
    cpf_cnpj = models.CharField(max_length=18)
    name = models.CharField(max_length=100)
    farm_name = models.CharField(max_length=100)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    city = models.CharField(max_length=100)
    farm_area_ha = models.DecimalField(max_digits=8, decimal_places=2)
    agro_area_ha = models.DecimalField(max_digits=8, decimal_places=2)
    veg_area_ha = models.DecimalField(max_digits=8, decimal_places=2)
    planting = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
