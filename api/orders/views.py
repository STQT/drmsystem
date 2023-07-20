from rest_framework import mixins, viewsets

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
