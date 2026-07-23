from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Order

from .tasks import generate_invoice_pdf

_status_before_save = {}

_payment_status_before_save = {}

@receiver(pre_save, sender=Order)
def capture_payment_status_before_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            _payment_status_before_save[instance.pk] = Order.objects.get(pk=instance.pk).payment_status
        except Order.DoesNotExist:
            _payment_status_before_save[instance.pk] = None

@receiver(post_save, sender=Order)
def trigger_invoice_generation(sender, instance, created, **kwargs):
    if created:
        return
    previous = _payment_status_before_save.pop(instance.pk, None)
    if previous != Order.PAYMENT_SUCCEEDED and instance.payment_status == Order.PAYMENT_SUCCEEDED:
        generate_invoice_pdf.delay(instance.pk)


@receiver(pre_save, sender=Order)
def capture_status_before_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            _status_before_save[instance.pk] = Order.objects.get(pk=instance.pk).status
        except Order.DoesNotExist:
            _status_before_save[instance.pk] = None


@receiver(post_save, sender=Order)
def broadcast_order_status_update(sender, instance, created, **kwargs):
    if created:
        return

    previous_status = _status_before_save.pop(instance.pk, None)
    if previous_status == instance.status:
        return

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"orders_user_{instance.user_id}",
        {
            "type": "order.status.update",
            "order_number": str(instance.order_number),
            "status": instance.status,
        },
    )