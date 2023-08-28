from rest_framework import mixins, viewsets, generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import Organization
from .serializers import UserSerializer, OrganizationSerializer
from rest_framework.pagination import PageNumberPagination

User = get_user_model()


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    max_page_size = 100


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == "list":
            qs = qs.filter(stopped=False).order_by('-last_login')
        return qs

    def create_or_update(self, request, *args, **kwargs):
        id_field = request.data.get('id')  # Assuming the 'id' field is sent in the request data
        if id_field:
            # Check if a user with the specified 'id' already exists
            user = User.objects.filter(id=id_field).first()
            if user:
                # If user with the 'id' already exists, update the user with the new data
                serializer = self.get_serializer(user, data=request.data, partial=True)
            else:
                # If user with the 'id' doesn't exist, create a new user
                serializer = self.get_serializer(data=request.data)
        else:
            # If 'id' field is not provided, create a new user
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def create(self, request, *args, **kwargs):
        return self.create_or_update(request, *args, **kwargs)


class OrganizationViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          mixins.UpdateModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all()
    lookup_field = "slug"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == 'list':
            return qs.filter(hide=False)
        return qs
