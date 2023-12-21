from django.urls import path
from apps.Venta.api import venta_api_view,reporte_ventas_api_view

urlpatterns = [
    path('ventas/', venta_api_view, name='ventas_api'),
    path('reporte_ventas/<str:fecha_inicio>/<str:fecha_fin>/', reporte_ventas_api_view, name='venta_detail_api_view'),
]