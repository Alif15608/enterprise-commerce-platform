from datetime import timedelta
from celery import shared_task
from django.utils import timezone

from .models import Cart

ABANDONED_CART_THRESHOLD_DAYS = 30


@shared_task
def cleanup_abandoned_guest_carts():
    """
    Runs daily via Celery Beat. Guest carts (no associated user) that
    haven't been touched in 30+ days are marked expired — they're never
    going anywhere at this point (the guest token was likely lost long ago),
    and leaving them ACTIVE indefinitely just accumulates dead rows.
    """
    cutoff = timezone.now() - timedelta(days=ABANDONED_CART_THRESHOLD_DAYS)
    updated_count = Cart.objects.filter(
        user__isnull=True, status=Cart.ACTIVE, updated_at__lt=cutoff,
    ).update(status=Cart.EXPIRED)
    return f"Expired {updated_count} abandoned guest cart(s)."