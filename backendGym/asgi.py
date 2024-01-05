import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendGym.settings.local')

application = get_asgi_application()
from apps.Registro.wsUrls import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": application,
        "websocket":AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)