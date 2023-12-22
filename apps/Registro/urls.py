from django.urls import path
from apps.Registro.api import registro_api_view,registro_detail_api_view,registros_api_view

urlpatterns = [
    path('registros/', registro_api_view, name='registros_api'),

    path('registros/<int:pk>', registro_detail_api_view, name='registro_detail_api_view'),
    path('registros/<str:fecha_inicio>/<str:fecha_fin>/', registros_api_view, name='registros_api_view'),
    
    path('registros/<int:pk>/<int:sus>', registro_detail_api_view, name='registro_detail_api_view'),
]