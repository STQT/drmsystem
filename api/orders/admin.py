from django.contrib import admin

from .models import Order, SubscriptionPrice, Subscriber


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "cost", "is_approved", "moderated_user", "created_at", "id"]
    ordering = ["-created_at"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ["user", "days", "created_at", "order"]
    raw_id_fields = ["user", "order"]


@admin.register(SubscriptionPrice)
class SubscriptionPriceAdmin(admin.ModelAdmin):
    ...
