from django.urls import path
from .views import listar_comandas, marcar_comanda_feita

urlpatterns = [
    path('listarcomandas/', listar_comandas, name='listar_comandas'),
    path('feita/<int:comanda_id>/', marcar_comanda_feita, name='marcar_comanda_feita'),
]
