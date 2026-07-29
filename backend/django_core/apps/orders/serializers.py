# apps/orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    line_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "product_sku", "unit_price", "quantity", "line_total"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_email = serializers.CharField(source="user.email", read_only=True)

    coupon_code = serializers.CharField(source="coupon.code", read_only=True, default=None)

    class Meta:
        model = Order
        fields = [
            "id", "order_number", "status", "payment_status",
            "subtotal", "discount_amount", "tax_amount", "shipping_cost", "total",
            "shipping_address", "items", "customer_email", "created_at", "coupon_code", 
        ]
        read_only_fields = fields


class CheckoutSerializer(serializers.Serializer):
    shipping_address_id = serializers.IntegerField()
    coupon_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class CouponValidateSerializer(serializers.Serializer):
    code = serializers.CharField()
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2)