from django.urls import path
from .views import fazer_pedido, listar_pedidos


urlpatterns = [
    path('fazer/', fazer_pedido, name='fazer_pedido'),
    path('pedidos/', listar_pedidos, name='listar_pedidos'),
]