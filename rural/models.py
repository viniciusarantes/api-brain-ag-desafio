from django.db import models

from rural.utils import STATE_CHOICES


class Producer(models.Model):
    cpf_cnpj = models.CharField(max_length=18)
    nome_produtor = models.CharField(max_length=100)
    nome_fazenda = models.CharField(max_length=100)
    estado = models.CharField(max_length=2, choices=STATE_CHOICES)
    cidade = models.CharField(max_length=100)
    area_fazenda_ha = models.DecimalField(max_digits=8, decimal_places=2)
    area_agricultavel_ha = models.DecimalField(max_digits=8, decimal_places=2)
    area_vegetacao_ha = models.DecimalField(max_digits=8, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)


class Planting(models.Model):
    nome = models.CharField(max_length=100)
    produtor = models.ManyToManyField(Producer)
    criado_em = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

