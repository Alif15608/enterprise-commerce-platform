from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Role, UserRole


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def assign_default_role(sender, instance, created, **kwargs):
    """
    Every newly created user gets the 'customer' role automatically.
    Runs regardless of HOW the user was created (registration, admin panel,
    createsuperuser, future bulk import) because it's hooked at the model
    level via post_save, not called explicitly from any one code path.
    """
    if not created:
        return

    try:
        customer_role = Role.objects.get(name=Role.CUSTOMER)
    except Role.DoesNotExist:
        # Roles haven't been seeded yet (e.g. first migration run,
        # before 0002_seed_roles has executed). Safe to skip silently.
        return

    UserRole.objects.get_or_create(user=instance, role=customer_role)