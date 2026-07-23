from celery import shared_task
from django.contrib.auth import get_user_model

from . import emails

User = get_user_model()


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_verification_email_task(self, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return  # user was deleted between scheduling and execution — nothing to do
    try:
        emails.send_verification_email(user)
    except Exception as exc:
        # Real SMTP providers occasionally have transient failures —
        # retry with backoff rather than silently losing the email.
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_password_reset_email_task(self, user_id, token):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return
    try:
        emails.send_password_reset_email(user, token)
    except Exception as exc:
        raise self.retry(exc=exc)