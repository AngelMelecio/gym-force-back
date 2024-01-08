from django.urls import path
from apps.Frase.api import frase_api_view,frase_detail_api_view

urlpatterns = [
    path('frases/', frase_api_view, name='frases_api'),
    path('frases/<int:pk>', frase_detail_api_view, name='frase_detail_api_view'),
]