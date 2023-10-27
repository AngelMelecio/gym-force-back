from rest_framework.routers import DefaultRouter

from apps.Users.api import UserViewSet

router = DefaultRouter()

router.register('', UserViewSet, basename="users")

urlpatterns = router.urls