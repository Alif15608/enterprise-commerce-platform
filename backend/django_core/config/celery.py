import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("enterprise_commerce")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "cleanup-abandoned-guest-carts": {
        "task": "apps.cart.tasks.cleanup_abandoned_guest_carts",
        "schedule": crontab(hour=3, minute=0),   # once daily, 3 AM
    },
    "generate-daily-sales-report": {
        "task": "apps.orders.tasks.generate_daily_sales_report",
        "schedule": crontab(hour=6, minute=0),   # once daily, 6 AM
    },
}