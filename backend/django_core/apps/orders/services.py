from django.db import transaction

from apps.catalog.models import Product
from apps.cart.models import Cart
from apps.accounts.models import Address
from .models import Order, OrderItem
from .payment import get_payment_gateway
from .pricing import calculate_tax, calculate_shipping


class CheckoutError(Exception):
    pass


@transaction.atomic
def checkout(*, user, cart: Cart, shipping_address_id: int):
    """
    The core checkout flow — validate, lock stock, charge, create order,
    all inside one atomic transaction. If ANYTHING fails partway through,
    the entire transaction rolls back: no partial stock decrement, no
    order created without payment, no cart wrongly marked converted.
    """
    if not cart.items.exists():
        raise CheckoutError("Cart is empty.")

    try:
        address = Address.objects.get(pk=shipping_address_id, user=user)
    except Address.DoesNotExist:
        raise CheckoutError("Shipping address not found for this user.")

    cart_items = list(cart.items.select_related("product"))

    # Lock every product row involved BEFORE checking stock, so no other
    # concurrent checkout can decrement between our check and our write.
    product_ids = [item.product_id for item in cart_items]
    locked_products = {
        p.id: p for p in Product.objects.select_for_update().filter(id__in=product_ids)
    }

    for item in cart_items:
        product = locked_products[item.product_id]
        if item.quantity > product.stock_quantity:
            raise CheckoutError(
                f"'{product.name}' only has {product.stock_quantity} unit(s) left — "
                f"please update your cart."
            )

    subtotal = sum((item.quantity * locked_products[item.product_id].price for item in cart_items), start=0)
    tax_amount = calculate_tax(subtotal)
    shipping_cost = calculate_shipping(subtotal)
    total = subtotal + tax_amount + shipping_cost

    order = Order.objects.create(
        user=user,
        shipping_address=address,
        subtotal=subtotal,
        tax_amount=tax_amount,
        shipping_cost=shipping_cost,
        total=total,
    )

    for item in cart_items:
        product = locked_products[item.product_id]
        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            product_sku=product.sku,
            unit_price=product.price,
            quantity=item.quantity,
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
        # Deliberately still raise, rolling back the whole transaction —
        # a failed charge should not leave decremented stock or a
        # half-created order behind.
        raise CheckoutError(f"Payment failed: {result.message}")

    order.save(update_fields=["payment_status", "status", "updated_at"])

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