import uuid
from django.db import transaction
from django.core.exceptions import ValidationError

from apps.catalog.models import Product
from .models import Cart, CartItem


class CartError(Exception):
    pass


def get_or_create_active_cart(*, user=None, session_token=None):
    """
    Returns the caller's active cart, creating one if none exists.
    Exactly one of user/session_token should be provided (view layer
    decides which, based on whether the request is authenticated).
    """
    if user is not None:
        cart, _ = Cart.objects.get_or_create(user=user, status=Cart.ACTIVE)
        return cart

    if session_token is None:
        session_token = uuid.uuid4()
        return Cart.objects.create(session_token=session_token, status=Cart.ACTIVE)

    cart, _ = Cart.objects.get_or_create(
        session_token=session_token, status=Cart.ACTIVE
    )
    return cart


def add_item(*, cart, product_id, quantity):
    try:
        product = Product.objects.get(pk=product_id, is_active=True, is_deleted=False)
    except Product.DoesNotExist:
        raise CartError("Product not found or unavailable.")

    existing_item = CartItem.objects.filter(cart=cart, product=product).first()
    requested_total = quantity + (existing_item.quantity if existing_item else 0)

    if requested_total > product.stock_quantity:
        raise CartError(
            f"Only {product.stock_quantity} unit(s) of '{product.name}' available."
        )

    if existing_item:
        existing_item.quantity = requested_total
        existing_item.save(update_fields=["quantity", "updated_at"])
        return existing_item

    return CartItem.objects.create(cart=cart, product=product, quantity=quantity)


def update_item_quantity(*, cart, item_id, quantity):
    try:
        item = CartItem.objects.select_related("product").get(pk=item_id, cart=cart)
    except CartItem.DoesNotExist:
        raise CartError("Cart item not found.")

    if quantity > item.product.stock_quantity:
        raise CartError(f"Only {item.product.stock_quantity} unit(s) available.")

    item.quantity = quantity
    item.save(update_fields=["quantity", "updated_at"])
    return item


def remove_item(*, cart, item_id):
    deleted_count, _ = CartItem.objects.filter(pk=item_id, cart=cart).delete()
    if deleted_count == 0:
        raise CartError("Cart item not found.")


def calculate_totals(*, cart):
    items = cart.items.select_related("product")
    subtotal = sum((item.line_total for item in items), start=0)
    return {
        "subtotal": subtotal,
        "item_count": sum(item.quantity for item in items),
        # discount/tax/shipping intentionally omitted here — discount arrives
        # with the Coupon phase, tax/shipping are computed at checkout
        # (Phase 9) once a real shipping address exists to calculate against.
    }


@transaction.atomic
def merge_guest_cart_into_user_cart(*, user, session_token):
    """
    Called right after login. Combines a guest cart's items into the
    user's cart, respecting stock limits, then marks the guest cart
    as merged (not deleted — kept for audit/debugging purposes).
    """
    try:
        guest_cart = Cart.objects.select_for_update().get(
            session_token=session_token, status=Cart.ACTIVE
        )
    except Cart.DoesNotExist:
        return  # nothing to merge — not an error, just a no-op

    user_cart, _ = Cart.objects.select_for_update().get_or_create(
        user=user, status=Cart.ACTIVE
    )

    for guest_item in guest_cart.items.select_related("product"):
        try:
            add_item(cart=user_cart, product_id=guest_item.product_id, quantity=guest_item.quantity)
        except CartError:
            # Stock ran out between guest adding it and merge happening —
            # skip this item rather than failing the entire merge.
            continue

    guest_cart.status = Cart.MERGED
    guest_cart.save(update_fields=["status", "updated_at"])
    return user_cart