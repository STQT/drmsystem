from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from api.main.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# USERS
router.register("users", UserViewSet)

app_name = "v1"
urlpatterns = router.urls
