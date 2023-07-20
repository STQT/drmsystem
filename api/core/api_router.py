from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from main.views import (UserViewSet, UserLocationsCreateAPIView, GetCategoriesAPIView, ProductsAPIView,  # noqa
                        RetrieveProductAPIView)  # noqa

from orders.views import OrderViewSet # noqa

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# USERS
router.register("users", UserViewSet)
router.register("products", ProductsAPIView)
router.register("orders", OrderViewSet)

app_name = "v1"
urlpatterns = router.urls

urlpatterns += [
    path('user-locations/', UserLocationsCreateAPIView.as_view(), name='location-create'),
    path('categories/', GetCategoriesAPIView.as_view(), name='categories-get'),
    path('product_by_name/<str:user_lang>/<str:name>', RetrieveProductAPIView.as_view(), name='product-by-name-get'),
]
