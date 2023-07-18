from uuid import uuid4

from django.db import models


class Order(models.Model):
    class PaymentMethods(models.TextChoices):
        CLICK = 'click', "Click UZ"
        PAYME = 'payme', "PayMe"
        CASH = 'cash', "Cash"

    id = models.UUIDField(editable=False, primary_key=True, default=uuid4)
    check_id = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=10, choices=PaymentMethods.choices, default=PaymentMethods.CASH)
    cost = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_products")
    product = models.ForeignKey("main.Product", on_delete=models.CASCADE, related_name="order_products")
    count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name_uz}, count={self.count}, order={self.order.id}"