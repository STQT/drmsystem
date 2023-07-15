from rest_framework import mixins, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from api.main.models import CustomUser, UserLocations, Category
from api.main.serializers import UserSerializer, UserLocationsSerializer, CategorySerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=True, methods=['get'])
    def get_locations(self, request, pk=None):
        instance = self.get_object()
        locations = instance.locations.all()
        serializer = UserLocationsSerializer(locations, many=True)
        serialized_data = serializer.data
        return Response(serialized_data)

    @action(detail=True, methods=['get'])
    def clear_locations(self, request, pk=None):
        instance = self.get_object()
        instance.locations.all().delete()
        return Response({"message": "ok"})


class UserLocationsCreateAPIView(generics.CreateAPIView):
    queryset = UserLocations.objects.all()
    serializer_class = UserLocationsSerializer


class GetCategoriesAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
