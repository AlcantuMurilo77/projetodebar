from django.shortcuts import render, redirect
from .models import Cliente, Produto, Pedido
from cozinha.models import Comanda
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Cliente, Produto, Pedido

def fazer_pedido(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        endereco = request.POST.get('endereco')
        produto_id = request.POST.get('produto')

        cliente = Cliente.objects.create(nome=nome, endereco=endereco)
        produto = Produto.objects.get(id=produto_id)

        
        pedido = Pedido.objects.create(cliente=cliente, produto=produto)

        Comanda.objects.create(
            pedido=pedido,
            produto=produto.nome,
            data_hora=timezone.now()
    )
        return redirect('listar_pedidos')
    
    produtos = Produto.objects.all()
    return render(request, 'fazer_pedido.html', {'produtos': produtos})


def listar_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'listar_pedidos.html', {'pedidos': pedidos})