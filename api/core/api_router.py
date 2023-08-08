from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from main.views import (UserViewSet, OrganizationViewSet)  # noqa

from orders.views import OrderViewSet, SubscriberAPIView, SubscriptionPriceAPIView  # noqa

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# USERS
router.register("users", UserViewSet)
router.register("orders", OrderViewSet)
router.register("subscriber", SubscriberAPIView)
router.register("prices", SubscriptionPriceAPIView)
router.register("organizations", OrganizationViewSet)

app_name = "v1"
urlpatterns = router.urls
