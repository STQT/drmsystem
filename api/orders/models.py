from django.utils import timezone
from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

User = get_user_model()


class Order(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)
    user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_DEFAULT,
                             default=1)
    photo = models.ImageField(blank=True, null=True)
    photo_uri = models.CharField(max_length=255, blank=True, null=True)
    cost = models.IntegerField()
    days = models.IntegerField()
    org = models.CharField(max_length=20)
    link = models.CharField(max_length=255, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    moderated_user = models.CharField(null=True, max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Юзер: " + str(self.user) + " | " + str(self.cost) + " тенге"


class SubscriptionPrice(models.Model):
    cost = models.IntegerField()
    days = models.IntegerField()

    def __str__(self):
        return str(self.days) + " күн " + str(self.cost) + " тенге"


class Subscriber(models.Model):
    user = models.OneToOneField(User, related_name='subscribers',
                                on_delete=models.SET_DEFAULT, default=1)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    days = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def expiration_date(self):
        return self.created_at + timezone.timedelta(days=self.days)

    def expiration_days(self):
        today = timezone.now().date()
        expiration = self.expiration_date().date()
        return (expiration - today).days + 1

    def is_subscription_expired(self):
        return timezone.now() > self.expiration_date()
