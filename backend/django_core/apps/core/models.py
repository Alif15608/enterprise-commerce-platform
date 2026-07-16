from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract base model providing created/updated timestamps.
    Every domain model in this project inherits from this.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    Abstract base model enabling soft deletes.
    Used for records where audit history matters (e.g. Orders, Products)
    rather than hard deletion.
    """
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True