from django.contrib.auth.models import AbstractBaseUser
from .managers import CustomUserManager
from django.db import models


class Category(models.Model):
    name_uz = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name_uz


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.IntegerField()
    photo = models.ImageField()
    name_uz = models.CharField(max_length=100)
    name_ru = models.CharField(max_length=100, blank=True, null=True)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    photo_uri = models.CharField(max_length=255, blank=True, null=True)
    massa = models.IntegerField(default=105)
    jirnost = models.IntegerField(default=15)
    temperature = models.IntegerField(default=18)
    srok_godnosti = models.IntegerField(default=18, help_text="Указывается в месяцах")
    upakovka = models.CharField(max_length=15, default="Флоу-Пак")
    protein = models.FloatField(default=3.7)
    fat = models.FloatField(default=14.4)
    carbohydrate = models.FloatField(default=24.2)
    calories = models.IntegerField(default=1008)
    description_uz = models.CharField(max_length=100)
    description_ru = models.CharField(max_length=100, blank=True, null=True)
    description_en = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name_uz


class CustomUser(AbstractBaseUser):
    id = models.IntegerField(primary_key=True)  # Using ID as primary key
    username = models.CharField(max_length=150, null=True)
    fullname = models.CharField(max_length=255)
    user_lang = models.CharField(max_length=2, default='uz')

    is_admin = models.BooleanField(default=False)

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


class UserLocations(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="locations")
    longitude = models.FloatField()
    latitude = models.FloatField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
