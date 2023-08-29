from django.contrib import admin

from .models import Order, SubscriptionPrice, Subscriber


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["user", "cost", "is_approved", "moderated_user", "created_at", "id"]
    raw_id_fields = ["user",]
    ordering = ["-created_at"]
    # readonly_fields = ["created_at"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ["user", "days", "created_at", "order", "get_order_org"]
    raw_id_fields = ["user", "order"]

    def get_order_org(self, obj):
        return obj.order.org

    get_order_org.short_description = "Org"

@admin.register(SubscriptionPrice)
class SubscriptionPriceAdmin(admin.ModelAdmin):
    ...
