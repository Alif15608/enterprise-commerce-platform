from rest_framework import serializers

from .models import Category, Brand, Product, ProductImage


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "children"]

    def get_children(self, obj):
        # Only serializes children if they were prefetched onto the instance
        # by the service layer's tree-building logic — avoids N+1 queries.
        children = getattr(obj, "_prefetched_children", [])
        return CategorySerializer(children, many=True).data


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "slug"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "is_primary", "display_order"]


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight — used for list endpoints. No description, no full image set."""
    primary_image = serializers.SerializerMethodField()
    is_in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price", "is_in_stock", "primary_image", "category", "brand"]

    def get_primary_image(self, obj):
        images = getattr(obj, "_prefetched_images", None)
        if not images:
            return None
        primary = next((img for img in images if img.is_primary), images[0] if images else None)
        return ProductImageSerializer(primary).data if primary else None


class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    is_in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "sku", "description", "price",
            "stock_quantity", "is_in_stock", "category", "brand", "images", "created_at",
        ]


class ProductWriteSerializer(serializers.ModelSerializer):
    """Used for create/update by Managers/Admins — separate from read serializers
    because writable fields (category id, brand id) differ from how we display
    them (nested objects) on read."""

    class Meta:
        model = Product
        fields = ["name", "sku", "description", "price", "stock_quantity", "category", "brand", "is_active"]