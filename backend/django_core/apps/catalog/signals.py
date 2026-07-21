import redis
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.orders.models import OrderItem

_redis_client = redis.from_url(settings.REDIS_URL_RAW)

POPULARITY_KEY = "popular:products"


@receiver(post_save, sender=OrderItem)
def track_product_popularity(sender, instance, created, **kwargs):
    if not created:
        return
    _redis_client.zincrby(POPULARITY_KEY, instance.quantity, str(instance.product_id))