
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

from django.urls import path,re_path
from django.views.static import serve

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.Users.views import Login,Logout


urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', Logout.as_view(), name = 'logout'),
    path('login/',Login.as_view(), name = 'login'),
    path('users/',include('apps.Users.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/',include('apps.Users.urls')),
    path('api/', include('apps.Suscripcion.urls')),
    path('api/', include('apps.Producto.urls')),
    path('api/', include('apps.Cliente.urls')),
    path('api/', include('apps.Registro.urls')),
    path('api/', include('apps.Venta.urls')),
    path('api/', include('apps.DetalleSuscripcion.urls')),
    path('api/', include('apps.Frase.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
