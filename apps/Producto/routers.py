from django.urls import path
from apps.Producto.api import producto_api_view, producto_detail_api_view

urlpatterns = [
    path('productos/', producto_api_view, name='producto_api_view'),
    path('productos/<int:pk>', producto_detail_api_view, name='producto_detail_api_view'),
]