from rest_framework import serializers

from apps.catalog.serializers import ProductListSerializer
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    line_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "line_total"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "session_token", "status", "items", "subtotal", "item_count"]

    def get_subtotal(self, obj):
        return sum((item.line_total for item in obj.items.all()), start=0)

    def get_item_count(self, obj):
        return sum(item.quantity for item in obj.items.all())


class AddItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class UpdateItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)