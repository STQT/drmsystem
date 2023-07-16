from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Product, UserLocations

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True}
        }


class UserLocationsSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserLocations
        fields = "__all__"
        extra_kwargs = {"user": {"required": False}}

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        name = validated_data.get("name")
        user = User.objects.get(id=user_id)
        try:
            instance = UserLocations.objects.get(user=user, name=name)
            return instance
        except UserLocations.DoesNotExist:
            validated_data["user"] = user
            instance = super().create(validated_data)
            return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
