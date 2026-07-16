from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class Role(TimeStampedModel):
    """
    A named permission grouping. Intentionally NOT a hardcoded choices field
    on User — new roles can be added by inserting a row, with zero migration
    required for the role set itself to grow.
    """
    ADMIN = "admin"
    MANAGER = "manager"
    SELLER = "seller"
    CUSTOMER = "customer"

    # These constants are used by our seed migration and permission classes
    # to reference well-known roles by a stable slug, without hardcoding
    # role *behavior* into the schema itself.
    name = models.SlugField(max_length=50, unique=True)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "roles"
        ordering = ["name"]

    def __str__(self):
        return self.name


class UserRole(TimeStampedModel):
    """
    Through model for the User <-> Role many-to-many relationship.
    Explicit through model (rather than a bare ManyToManyField) so we can
    later add fields like `granted_by` or `expires_at` without a schema
    rewrite — a common real-world RBAC requirement we're leaving room for.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles")

    class Meta:
        db_table = "user_roles"
        constraints = [
            models.UniqueConstraint(fields=["user", "role"], name="unique_user_role"),
        ]
        indexes = [
            models.Index(fields=["user", "role"]),
        ]