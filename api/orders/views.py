from rest_framework import mixins, viewsets
from rest_framework.parsers import MultiPartParser

from .models import Order, Subscriber, SubscriptionPrice
from .serializers import OrderSerializer, SubscriberSerializer, SubscriptionPriceSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filterset_fields = ["user__id"]


class SubscriberAPIView(mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = SubscriberSerializer
    queryset = Subscriber.objects.all().select_related("user")
    lookup_field = "user__id"


class SubscriptionPriceAPIView(mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    serializer_class = SubscriptionPriceSerializer
    queryset = SubscriptionPrice.objects.all()


