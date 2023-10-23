from django.urls import path
from apps.Cliente.api import cliente_api_view, cliente_detail_api_view

urlpatterns = [
    path('clientes/', cliente_api_view, name='cliente_api_view'),
    path('clientes/<int:pk>', cliente_detail_api_view, name='cliente_detail_api_view'),
]