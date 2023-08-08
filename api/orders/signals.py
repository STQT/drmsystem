from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

from .tasks import getting_order_photo, create_subscription
from .models import Order, Subscriber


@receiver(post_save, sender=Order)
def OrderCreatePhoto(sender, instance, created, **kwargs):
    if created:
        getting_order_photo.delay(instance.id)


@receiver(post_save, sender=Order)
def OrderSubscriberCreate(sender, instance, created, **kwargs):
    if instance.is_approved:
        create_subscription.delay(instance.id, instance.user.id, instance.days)


@receiver(pre_delete, sender=Subscriber)
def update_user_subscription_status(sender, instance, **kwargs):
    instance.user.is_subscribed = False
    instance.user.save()
