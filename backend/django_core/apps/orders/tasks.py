import io
from datetime import date, timedelta
from decimal import Decimal

from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .models import Order


@shared_task(bind=True, max_retries=3, default_retry_delay=120)
def generate_invoice_pdf(self, order_id):
    try:
        order = Order.objects.prefetch_related("items").get(pk=order_id)
    except Order.DoesNotExist:
        return

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, 750, f"Invoice — Order {order.order_number}")
    p.setFont("Helvetica", 10)
    p.drawString(50, 730, f"Date: {order.created_at.strftime('%Y-%m-%d')}")
    p.drawString(50, 715, f"Customer: {order.user.email}")

    y = 680
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Item")
    p.drawString(300, y, "Qty")
    p.drawString(360, y, "Unit Price")
    p.drawString(460, y, "Line Total")
    y -= 20
    p.setFont("Helvetica", 10)

    for item in order.items.all():
        p.drawString(50, y, item.product_name[:40])
        p.drawString(300, y, str(item.quantity))
        p.drawString(360, y, f"${item.unit_price}")
        p.drawString(460, y, f"${item.line_total}")
        y -= 18

    y -= 10
    p.line(50, y, 550, y)
    y -= 20
    p.drawString(360, y, "Subtotal:")
    p.drawString(460, y, f"${order.subtotal}")
    y -= 18
    p.drawString(360, y, "Tax:")
    p.drawString(460, y, f"${order.tax_amount}")
    y -= 18
    p.drawString(360, y, "Shipping:")
    p.drawString(460, y, f"${order.shipping_cost}")
    y -= 18
    p.setFont("Helvetica-Bold", 11)
    p.drawString(360, y, "Total:")
    p.drawString(460, y, f"${order.total}")

    p.showPage()
    p.save()
    buffer.seek(0)

    email = EmailMessage(
        subject=f"Invoice for Order {order.order_number}",
        body="Please find your invoice attached.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[order.user.email],
    )
    email.attach(f"invoice_{order.order_number}.pdf", buffer.read(), "application/pdf")
    email.send()


@shared_task
def generate_daily_sales_report():
    """
    Runs daily via Celery Beat (see config/celery.py schedule).
    Aggregates yesterday's paid orders and emails a summary to Admins.
    """
    from apps.rbac.models import Role

    yesterday = date.today() - timedelta(days=1)
    orders = Order.objects.filter(
        created_at__date=yesterday, payment_status=Order.PAYMENT_SUCCEEDED,
    )

    total_revenue = sum((o.total for o in orders), start=Decimal("0"))
    order_count = orders.count()

    admin_emails = list(
        Order._meta.apps.get_model("accounts", "User")
        .objects.filter(user_roles__role__name=Role.ADMIN)
        .values_list("email", flat=True)
    )

    if not admin_emails:
        return

    body = (
        f"Sales Report for {yesterday}\n\n"
        f"Orders placed: {order_count}\n"
        f"Total revenue: ${total_revenue}\n"
    )
    EmailMessage(
        subject=f"Daily Sales Report — {yesterday}",
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=admin_emails,
    ).send()