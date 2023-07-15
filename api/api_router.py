from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from api.main.views import UserViewSet, UserLocationsCreateAPIView, GetCategoriesAPIView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# USERS
router.register("users", UserViewSet)

app_name = "v1"
urlpatterns = router.urls

urlpatterns += [
    path('user-locations/', UserLocationsCreateAPIView.as_view(), name='location-create'),
    path('categories/', GetCategoriesAPIView.as_view(), name='categories-get'),
]
