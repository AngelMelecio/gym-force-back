from django.urls import path
from apps.Almacen.api import almacen_api_view,almacen_detail_api_view

urlpatterns = [
    path('almacens/', almacen_api_view, name='almacens_api'),
    path('almacens/<int:pk>', almacen_detail_api_view, name='almacen_detail_api_view'),
]