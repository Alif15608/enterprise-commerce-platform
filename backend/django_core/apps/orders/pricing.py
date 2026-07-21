from decimal import Decimal

# Placeholder constants — real tax/shipping logic (jurisdiction-based rates,
# carrier APIs) is out of scope for this phase. Isolated here specifically
# so it's obvious this is a stand-in, not scattered inline in services.py.
FLAT_TAX_RATE = Decimal("0.08")
FLAT_SHIPPING_COST = Decimal("5.00")
FREE_SHIPPING_THRESHOLD = Decimal("50.00")


def calculate_tax(subtotal: Decimal) -> Decimal:
    return (subtotal * FLAT_TAX_RATE).quantize(Decimal("0.01"))


def calculate_shipping(subtotal: Decimal) -> Decimal:
    if subtotal >= FREE_SHIPPING_THRESHOLD:
        return Decimal("0.00")
    return FLAT_SHIPPING_COST