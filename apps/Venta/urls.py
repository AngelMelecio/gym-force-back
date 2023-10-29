from django.urls import path
from apps.Venta.api import venta_api_view,venta_detail_api_view

urlpatterns = [
    path('ventas/', venta_api_view, name='ventas_api'),
    path('ventas/<int:pk>', venta_detail_api_view, name='venta_detail_api_view'),
]