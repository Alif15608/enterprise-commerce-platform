from decimal import Decimal

from django.db import transaction
from django.db.models import F
from django.utils import timezone

from apps.accounts.models import Address
from apps.cart.models import Cart
from apps.catalog.models import Product

from .models import Coupon, Order, OrderItem
from .payment import get_payment_gateway
from .pricing import calculate_shipping, calculate_tax


class CheckoutError(Exception):
    pass

class CouponError(Exception):
    pass


@transaction.atomic
def checkout(*, user, cart: Cart, shipping_address_id: int, coupon_code: str | None = None):
    if not cart.items.exists():
        raise CheckoutError("Cart is empty.")

    try:
        address = Address.objects.get(pk=shipping_address_id, user=user)
    except Address.DoesNotExist:
        raise CheckoutError("Shipping address not found for this user.")

    cart_items = list(cart.items.select_related("product"))
    product_ids = [item.product_id for item in cart_items]
    locked_products = {
        p.id: p for p in Product.objects.select_for_update().filter(id__in=product_ids)
    }

    for item in cart_items:
        product = locked_products[item.product_id]
        if item.quantity > product.stock_quantity:
            raise CheckoutError(
                f"'{product.name}' only has {product.stock_quantity} unit(s) left — please update your cart."
            )

    subtotal = sum((item.quantity * locked_products[item.product_id].price for item in cart_items), start=0)

    coupon = None
    discount_amount = 0
    if coupon_code:
        try:
            coupon, discount_amount = validate_coupon(code=coupon_code, subtotal=subtotal)
        except CouponError as e:
            raise CheckoutError(str(e))

    tax_amount = calculate_tax(subtotal - discount_amount)
    shipping_cost = calculate_shipping(subtotal - discount_amount)
    total = subtotal - discount_amount + tax_amount + shipping_cost

    order = Order.objects.create(
        user=user,
        shipping_address=address,
        coupon=coupon,
        subtotal=subtotal,
        discount_amount=discount_amount,
        tax_amount=tax_amount,
        shipping_cost=shipping_cost,
        total=total,
    )

    for item in cart_items:
        product = locked_products[item.product_id]
        OrderItem.objects.create(
            order=order, product=product, product_name=product.name,
            product_sku=product.sku, unit_price=product.price, quantity=item.quantity,
        )
        product.stock_quantity -= item.quantity
        product.save(update_fields=["stock_quantity", "updated_at"])

    gateway = get_payment_gateway()
    result = gateway.charge(order=order, amount=total)

    if result.success:
        order.payment_status = Order.PAYMENT_SUCCEEDED
        order.status = Order.PAID
    else:
        order.payment_status = Order.PAYMENT_FAILED
        raise CheckoutError(f"Payment failed: {result.message}")

    order.save(update_fields=["payment_status", "status", "updated_at"])

    if coupon:
        consume_coupon(coupon=coupon)  # only consumed on a genuinely successful order

    cart.status = Cart.CONVERTED
    cart.save(update_fields=["status", "updated_at"])

    return order


def get_orders_for_user(*, user):
    return Order.objects.filter(user=user).prefetch_related("items").order_by("-created_at")


def get_order_detail(*, user, order_number, is_staff=False):
    qs = Order.objects.prefetch_related("items__product")
    if not is_staff:
        qs = qs.filter(user=user)
    try:
        return qs.get(order_number=order_number)
    except Order.DoesNotExist:
        raise CheckoutError("Order not found.")

def update_order_status(*, order_number, new_status, is_staff):
    if not is_staff:
        raise CheckoutError("Not authorized to update order status.")
    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        raise CheckoutError("Order not found.")
    order.status = new_status
    order.save(update_fields=["status", "updated_at"])
    return order

def validate_coupon(*, code, subtotal):
    """
    Returns the discount amount a coupon would apply against a given
    subtotal, without consuming a use. Called both by a standalone
    preview endpoint and internally by checkout() itself.
    """
    try:
        coupon = Coupon.objects.get(code__iexact=code, is_active=True)
    except Coupon.DoesNotExist:
        raise CouponError("Invalid coupon code.")

    now = timezone.now()
    if not (coupon.valid_from <= now <= coupon.valid_until):
        raise CouponError("This coupon has expired or is not yet active.")

    if coupon.max_uses is not None and coupon.times_used >= coupon.max_uses:
        raise CouponError("This coupon has reached its usage limit.")

    if coupon.discount_type == Coupon.PERCENTAGE:
        discount = (subtotal * coupon.amount / 100).quantize(Decimal("0.01"))
    else:
        discount = min(coupon.amount, subtotal)  # never discount below zero

    return coupon, discount


def consume_coupon(*, coupon):
    """
    Atomically increments usage count — F() expression avoids a
    read-then-write race identical in spirit to Phase 9's stock locking.
    """
    Coupon.objects.filter(pk=coupon.pk).update(times_used=F("times_used") + 1)
