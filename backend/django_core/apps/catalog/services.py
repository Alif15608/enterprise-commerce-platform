from django.core.cache import cache
from django.db.models import Prefetch

from .models import Category, Product, ProductImage
from .cache import (
    make_product_list_cache_key, make_category_tree_cache_key,
    bump_products_cache_version, bump_categories_cache_version, DEFAULT_CACHE_TTL,
)


def get_category_tree():
    """
    Builds the full category tree in memory from a single flat query,
    rather than N recursive queries (one per level) — avoids the N+1
    problem that a naive recursive ORM traversal would cause.
    """
    cache_key = make_category_tree_cache_key()
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    all_categories = list(Category.objects.filter(is_active=True).order_by("name"))
    by_parent = {}
    for cat in all_categories:
        by_parent.setdefault(cat.parent_id, []).append(cat)

    def attach_children(category):
        category._prefetched_children = by_parent.get(category.id, [])
        for child in category._prefetched_children:
            attach_children(child)

    roots = by_parent.get(None, [])
    for root in roots:
        attach_children(root)

    cache.set(cache_key, roots, timeout=DEFAULT_CACHE_TTL)
    return roots


def get_product_queryset():
    """Base queryset for published, non-deleted products, with related
    objects prefetched to avoid N+1 queries in the serializer layer."""
    return (
        Product.objects
        .filter(is_active=True, is_deleted=False)
        .select_related("category", "brand")
        .prefetch_related(Prefetch("images", queryset=ProductImage.objects.order_by("display_order")))
    )


def create_product(*, category_id, sku, name, price, stock_quantity=0, brand_id=None, description="", is_active=True):
    product = Product.objects.create(
        category_id=category_id,
        brand_id=brand_id,
        name=name,
        sku=sku,
        description=description,
        price=price,
        stock_quantity=stock_quantity,
        is_active=is_active,
    )
    bump_products_cache_version()
    return product


def update_product(*, product, **fields):
    for key, value in fields.items():
        setattr(product, key, value)
    product.save()
    bump_products_cache_version()
    return product


def soft_delete_product(*, product):
    product.is_deleted = True
    product.is_active = False
    product.save(update_fields=["is_deleted", "is_active", "updated_at"])
    bump_products_cache_version()