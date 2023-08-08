from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from orders.models import Order, Subscriber

User = get_user_model()


@receiver(post_delete, sender=User)
def set_default_user(sender, instance, **kwargs):
    Order.objects.filter(user=instance).update(user_id=1)
    Subscriber.objects.filter(user=instance).update(user_id=1)
