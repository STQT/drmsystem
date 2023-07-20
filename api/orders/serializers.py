from rest_framework import serializers

from main.models import Product  # noqa
from orders.models import OrderProduct, Order  # noqa


def get_product_by_name_and_lang(name, lang):
    try:
        return Product.objects.get(**{f"name_{lang}": name})
    except Product.DoesNotExist:
        raise serializers.ValidationError(f"Product with name '{name}' and lang '{lang}' not found.")


class OrderProductSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    product_name = serializers.CharField()
    product_lang = serializers.ChoiceField(choices=[('uz', 'uz'), ('ru', 'ru'), ('en', 'en')])

    # class Meta:
    #     model = OrderProduct
    #     fields = ('product_name', 'product_lang', 'count')
    #
    # def create(self, validated_data):
    #     product_name = validated_data.pop('product_name')
    #     product_lang = validated_data.pop('product_lang')
    #     print(validated_data)
    #     product = get_product_by_name_and_lang(product_name, product_lang)
    #     return OrderProduct(product=product, **validated_data)


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, write_only=True, source="order_products")  # Nested serializer for OrderProduct

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        products_data = validated_data.pop('order_products')
        order = super().create(validated_data)
        for product_data in products_data:
            product_name = product_data.pop('product_name')
            product_lang = product_data.pop('product_lang')
            print(product_data)
            product = get_product_by_name_and_lang(product_name, product_lang)
            OrderProduct.objects.create(order=order, product=product, **product_data)
        return order
