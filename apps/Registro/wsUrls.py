from django.urls import re_path
from .consumers import AccessConsumer

websocket_urlpatterns = [
    re_path(r'ws/access/(?P<room_name>\w+)/$', AccessConsumer.as_asgi()),
]