from rest_framework import mixins, viewsets

from api.main.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
