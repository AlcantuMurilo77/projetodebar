from django.db import models

from django.db import models
from delivery.models import Pedido

class Comanda(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=100)
    data_hora = models.DateTimeField()

    def __str__(self):
        return f'{self.produto} - {self.data_hora.strftime("%d/%m %H:%M")}'
