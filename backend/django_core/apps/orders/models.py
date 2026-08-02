import uuid

from django.conf import settings
from django.db import models

from apps.accounts.models import Address
from apps.catalog.models import Product
from apps.core.models import TimeStampedModel


class Coupon(TimeStampedModel):
    PERCENTAGE = "percentage"
    FLAT = "flat"
    DISCOUNT_TYPE_CHOICES = [(PERCENTAGE, "Percentage"), (FLAT, "Flat amount")]

    code = models.CharField(max_length=32, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # e.g. 10.00 = 10% or $10

    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()

    max_uses = models.PositiveIntegerField(null=True, blank=True)  # null = unlimited
    times_used = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "coupons"
        constraints = [
            models.CheckConstraint(check=models.Q(amount__gt=0), name="coupon_amount_positive"),
        ]

    def __str__(self):
        return self.code

class Order(TimeStampedModel):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (PENDING, "Pending"), (PAID, "Paid"), (SHIPPED, "Shipped"),
        (DELIVERED, "Delivered"), (CANCELLED, "Cancelled"),
    ]

    PAYMENT_PENDING = "pending"
    PAYMENT_SUCCEEDED = "succeeded"
    PAYMENT_FAILED = "failed"
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING, "Pending"), (PAYMENT_SUCCEEDED, "Succeeded"), (PAYMENT_FAILED, "Failed"),
    ]

    order_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="orders", on_delete=models.PROTECT)
    shipping_address = models.ForeignKey(Address, related_name="+", on_delete=models.PROTECT)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_PENDING)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    coupon = models.ForeignKey(Coupon, null=True, blank=True, on_delete=models.SET_NULL, related_name="orders")

    class Meta:
        db_table = "orders"
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["order_number"]),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(total__gte=0), name="order_total_non_negative"),
        ]

    def __str__(self):
        return f"Order {self.order_number} ({self.status})"


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.PROTECT)

    # Snapshotted at order time — see Decision 2. These deliberately do NOT
    # update if the underlying Product changes later.
    product_name = models.CharField(max_length=255)
    product_sku = models.CharField(max_length=64)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = "order_items"
        indexes = [models.Index(fields=["order"])]


    @property
    def line_total(self):
        if self.unit_price is None or self.quantity is None:
            return None
        return self.unit_price * self.quantity
