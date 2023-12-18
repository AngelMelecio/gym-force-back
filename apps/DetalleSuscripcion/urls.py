from django.urls import path
from apps.DetalleSuscripcion.api import ds_change_date_end_api_view

urlpatterns = [
    path('detalleSuscripcionNft/<int:pk>', ds_change_date_end_api_view, name='ds_change_date_end_api_view'),
]