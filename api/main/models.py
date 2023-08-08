from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager
from django.db import models

from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings


class CustomUser(AbstractBaseUser):
    id = models.PositiveBigIntegerField(primary_key=True)  # Using ID as primary key
    username = models.CharField(max_length=150, null=True)
    fullname = models.CharField(max_length=255)
    user_lang = models.CharField(max_length=2, default='kz')

    is_admin = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)
    stopped = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'id'  # Using ID as the authentication field
    REQUIRED_FIELDS = ['fullname']  # Other required fields for creating a user

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return str(self.id)


class Organization(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField()
    photo_uri = models.CharField(max_length=255, null=True, blank=True)
    photo_updated = models.BooleanField(default=False)
    group_id = models.CharField(max_length=20)
    kaspi = models.CharField(max_length=12)
    hide = models.BooleanField(default=False)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if the photo field has changed
        if self.pk is not None:
            original_photo = Organization.objects.get(pk=self.pk).photo
            if original_photo and original_photo != self.photo:
                self.photo_updated = True

        super(Organization, self).save(*args, **kwargs)


@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def set_default_user(sender, instance, **kwargs):
    instance.orders.update(user_id=1)
    instance.subscribers.update(user_id=1)
