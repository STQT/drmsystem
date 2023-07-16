from django.http import Http404
from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Product
from .serializers import UserSerializer, UserLocationsSerializer, CategorySerializer, ProductSerializer
from django.contrib.auth import get_user_model

from .models import UserLocations

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


class ProductsAPIView(mixins.ListModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = (
        'category__name_uz',
        'category__name_ru',
        'category__name_en',
    )


class RetrieveProductAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_object(self):

        queryset = self.get_queryset()

        lang = self.kwargs['user_lang']
        name = self.kwargs['name']
        name_key = "name_" + lang
        try:
            return queryset.get(
                **{name_key: name}
            )
        except Product.DoesNotExist:
            raise Http404(
                "No %s matches the given query." % Product._meta.object_name
            )
