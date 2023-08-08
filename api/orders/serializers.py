import logging

import requests

from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers, status

from orders.models import SubscriptionPrice, Subscriber, Order  # noqa
from django.utils import timezone

User = get_user_model()


class OrderSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Order
        fields = "__all__"
        extra_kwargs = {"user": {"required": False}}

    def create(self, validated_data):
        user_id = validated_data.pop("user_id")
        user = User.objects.get(id=user_id)
        current_datetime = timezone.localtime(timezone.now())

        # Extract the date from the datetime object
        today = current_datetime.date()
        creations_today = Order.objects.filter(user=user, created_at__date=today).count()
        print(creations_today)
        if creations_today >= 3:
            error_message = "You have reached the limit of 3 creations per day."
            raise serializers.ValidationError({"error": error_message})
        validated_data["user"] = user
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if instance.is_approved is False:
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

            # Payload for the request
            data = {
                "chat_id": instance.user.id,
                "text": f"Вам отказали в подписке"
            }
            response = requests.post(url, data=data)

            # Check if the request was successful
            if response.status_code == 200:
                logging.info("Message sent successfully.")
            else:
                logging.warning(f"Failed to send message. Status code: {response.status_code}")
                logging.warning(response.text)
        return instance


class SubscriptionPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPrice
        fields = "__all__"


class SubscriberSerializer(serializers.ModelSerializer):
    expiration_days = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subscriber
        fields = "__all__"

    def get_expiration_days(self, instance):
        return instance.expiration_days()
