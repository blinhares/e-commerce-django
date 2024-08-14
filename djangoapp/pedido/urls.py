from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path("",views.Pagar.as_view(), name = "pagar" ),
    path("",views.FecharPedido.as_view(), name = "fecharpedido" ),
    path("",views.Detalhe.as_view(), name = "detalhe" ),
    
]
