from django.urls import path
from apps.Appname.api import appname_api_view,appname_detail_api_view

urlpatterns = [
    path('appnames/', appname_api_view, name='appnames_api'),
    path('appnames/<int:pk>', appname_detail_api_view, name='appname_detail_api_view'),
]