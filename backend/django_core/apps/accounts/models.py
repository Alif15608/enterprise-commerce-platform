from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.core.models import TimeStampedModel
from .managers import UserManager

from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """
    Custom user model, authenticated by email instead of username.

    We deliberately do NOT add a `role` field here yet — that belongs to
    the RBAC phase (Phase 6), where we'll design it properly (a separate
    Role model + M2M, rather than a hardcoded choices field) so permissions
    can scale beyond four hardcoded roles without another migration.
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # email + password already required by USERNAME_FIELD/AbstractBaseUser

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        return self.email

class Address(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="addresses", on_delete=models.CASCADE)

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = "addresses"
        indexes = [models.Index(fields=["user"])]

    def __str__(self):
        return f"{self.full_name}, {self.city}, {self.country}"