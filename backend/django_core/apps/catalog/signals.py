import redis
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.orders.models import OrderItem

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Product

_redis_client = redis.from_url(settings.REDIS_URL_RAW)

POPULARITY_KEY = "popular:products"


@receiver(post_save, sender=OrderItem)
def track_product_popularity(sender, instance, created, **kwargs):
    if not created:
        return
    _redis_client.zincrby(POPULARITY_KEY, instance.quantity, str(instance.product_id))



# Alongside the existing Phase 11 import of OrderItem/popularity tracking...

_stock_before_save = {}


@receiver(pre_save, sender=Product)
def capture_stock_before_save(sender, instance, **kwargs):
    """
    Records the product's current DB stock value right before a save,
    so post_save can detect whether stock actually changed — Django gives
    us no built-in 'old value' access inside post_save otherwise.
    """
    if instance.pk:
        try:
            _stock_before_save[instance.pk] = Product.objects.get(pk=instance.pk).stock_quantity
        except Product.DoesNotExist:
            _stock_before_save[instance.pk] = None


@receiver(post_save, sender=Product)
def broadcast_inventory_update(sender, instance, created, **kwargs):
    if created:
        return

    previous_stock = _stock_before_save.pop(instance.pk, None)
    if previous_stock == instance.stock_quantity:
        return  # nothing changed — don't spam connected clients

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"inventory_{instance.pk}",
        {
            "type": "inventory.update",
            "product_id": instance.pk,
            "stock_quantity": instance.stock_quantity,
        },
    )