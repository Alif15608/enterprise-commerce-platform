from django.contrib.auth import get_user_model

from .models import Role, UserRole

User = get_user_model()


class RbacError(Exception):
    pass


def assign_role(*, user_id, role_name):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise RbacError("User not found.")

    try:
        role = Role.objects.get(name=role_name)
    except Role.DoesNotExist:
        raise RbacError(f"Role '{role_name}' does not exist.")

    user_role, created = UserRole.objects.get_or_create(user=user, role=role)
    return user_role, created


def revoke_role(*, user_id, role_name):
    deleted_count, _ = UserRole.objects.filter(
        user_id=user_id, role__name=role_name
    ).delete()
    if deleted_count == 0:
        raise RbacError("User does not have that role.")


def get_user_roles(*, user_id):
    return Role.objects.filter(user_roles__user_id=user_id)