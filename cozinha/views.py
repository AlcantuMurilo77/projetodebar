from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from .models import Comanda

def listar_comandas(request):
    comandas = Comanda.objects.all().order_by('-data_hora')
    return render(request, 'listar_comandas.html', {'comandas': comandas})

def marcar_comanda_feita(request, comanda_id):
    comanda = get_object_or_404(Comanda, id=comanda_id)
    comanda.delete()
    return redirect('listar_comandas')
