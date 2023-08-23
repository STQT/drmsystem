from django.urls import path, include
from .views import dashboard, get_orders_data, get_subscribers_data, get_detail_organization

urlpatterns = [
    path("", dashboard, name="v1"),
    path("get_orders_data/", get_orders_data, name="get_order_data"),
    path("get_subscribers_data/", get_subscribers_data, name="get_subscriber_data"),
    path("organizations/<slug:slug>/", get_detail_organization, name="organization"),
]