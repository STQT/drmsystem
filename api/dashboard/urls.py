from django.urls import path, include
from .views import dashboard, get_orders_data, get_subscribers_data

urlpatterns = [
    path("", dashboard, name="v1"),
    path("get_orders_data/", get_orders_data, name="v1"),
    path("get_subscribers_data/", get_subscribers_data, name="v1"),

]