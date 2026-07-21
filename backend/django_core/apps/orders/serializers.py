from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    line_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "product_sku", "unit_price", "quantity", "line_total"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "order_number", "status", "payment_status",
            "subtotal", "discount_amount", "tax_amount", "shipping_cost", "total",
            "shipping_address", "items", "created_at",
        ]
        read_only_fields = fields


class CheckoutSerializer(serializers.Serializer):
    shipping_address_id = serializers.IntegerField()