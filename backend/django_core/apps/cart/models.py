import uuid
from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel
from apps.catalog.models import Product


class Cart(TimeStampedModel):
    ACTIVE = "active"
    MERGED = "merged"
    CONVERTED = "converted"   # set to this in Phase 9 once an Order is placed from it

    STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (MERGED, "Merged into another cart"),
        (CONVERTED, "Converted to order"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        related_name="carts", on_delete=models.CASCADE,
    )
    session_token = models.UUIDField(null=True, blank=True, default=None)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ACTIVE)

    class Meta:
        db_table = "carts"
        constraints = [
            models.CheckConstraint(
                check=models.Q(user__isnull=False) | models.Q(session_token__isnull=False),
                name="cart_has_owner",
            ),
            models.UniqueConstraint(
                fields=["user"], condition=models.Q(status="active"),
                name="unique_active_cart_per_user",
            ),
            models.UniqueConstraint(
                fields=["session_token"], condition=models.Q(status="active"),
                name="unique_active_cart_per_session_token",
            ),
        ]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["session_token", "status"]),
        ]

    def __str__(self):
        owner = self.user.email if self.user else f"guest:{self.session_token}"
        return f"Cart({owner}, {self.status})"


class CartItem(TimeStampedModel):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="cart_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "cart_items"
        constraints = [
            models.UniqueConstraint(fields=["cart", "product"], name="unique_product_per_cart"),
            models.CheckConstraint(check=models.Q(quantity__gte=1), name="cart_item_quantity_positive"),
        ]
        indexes = [
            models.Index(fields=["cart"]),
        ]

    @property
    def line_total(self):
        return self.product.price * self.quantity