from django.urls import path
from apps.Suscripcion.api import suscripcion_api_view, suscripcion_detail_api_view

urlpatterns = [
    path('suscripciones/', suscripcion_api_view, name='suscripcion_api_view'),
    path('suscripciones/<int:pk>', suscripcion_detail_api_view, name='suscripcion_detail_api_view'),
]