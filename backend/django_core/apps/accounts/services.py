from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken

from .tokens import email_verification_token
from .emails import send_verification_email, send_password_reset_email

from .models import Address

from .tasks import send_verification_email_task, send_password_reset_email_task

User = get_user_model()


class AuthenticationError(Exception):
    """Raised for auth business-rule violations that aren't simple field validation."""
    pass


def register_user(*, email, password, first_name="", last_name=""):
    """
    Creates a new, inactive user and sends a verification email.
    The user cannot log in until verify_email() succeeds.
    """
    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        is_active=False,
    )
    send_verification_email_task.delay(user.id)   # was: send_verification_email(user)
    return user

def verify_email(*, uid, token):
    try:
        user_pk = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=user_pk)
    except (ObjectDoesNotExist, ValueError, TypeError, OverflowError):
        raise AuthenticationError("Invalid verification link.")

    if not email_verification_token.check_token(user, token):
        raise AuthenticationError("Invalid or expired verification link.")

    user.is_active = True
    user.save(update_fields=["is_active"])
    return user


def issue_tokens_for_user(user):
    """
    Issues a fresh access/refresh token pair. Used by both login and
    email verification (if we later decide to auto-login on verify).
    """
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def logout_user(*, refresh_token):
    """
    Blacklists the given refresh token, making it permanently unusable —
    this is what makes logout actually invalidate the session server-side,
    rather than just relying on the frontend to discard the token.
    """
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception:
        raise AuthenticationError("Invalid refresh token.")


def change_password(*, user, old_password, new_password):
    if not user.check_password(old_password):
        raise AuthenticationError("Current password is incorrect.")
    user.set_password(new_password)
    user.save(update_fields=["password"])


def request_password_reset(*, email):
    """
    Always succeeds from the caller's perspective, even if the email
    doesn't exist — this prevents user enumeration (an attacker probing
    which emails are registered by watching for different responses).
    """
    try:
        user = User.objects.get(email=email, is_active=True)
    except User.DoesNotExist:
        return  # silently no-op — same external behavior either way

    token = default_token_generator.make_token(user)
    send_password_reset_email_task.delay(user.id, token)   # was: send_password_reset_email(user, token)


def confirm_password_reset(*, uid, token, new_password):
    try:
        user_pk = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=user_pk)
    except (ObjectDoesNotExist, ValueError, TypeError, OverflowError):
        raise AuthenticationError("Invalid reset link.")

    if not default_token_generator.check_token(user, token):
        raise AuthenticationError("Invalid or expired reset link.")

    user.set_password(new_password)
    user.save(update_fields=["password"])


def list_addresses(*, user):
    return user.addresses.all()


def create_address(*, user, is_default=False, **fields):
    if is_default:
        # Only one address can be default at a time — unset any existing
        # default before creating this one, so the invariant always holds.
        Address.objects.filter(user=user, is_default=True).update(is_default=False)
    return Address.objects.create(user=user, is_default=is_default, **fields)


def update_address(*, user, address_id, is_default=None, **fields):
    try:
        address = Address.objects.get(pk=address_id, user=user)
    except Address.DoesNotExist:
        raise AuthenticationError("Address not found.")

    if is_default is True:
        Address.objects.filter(user=user, is_default=True).exclude(pk=address.pk).update(is_default=False)
        fields["is_default"] = True
    elif is_default is False:
        fields["is_default"] = False

    for key, value in fields.items():
        setattr(address, key, value)
    address.save()
    return address


def delete_address(*, user, address_id):
    deleted_count, _ = Address.objects.filter(pk=address_id, user=user).delete()
    if deleted_count == 0:
        raise AuthenticationError("Address not found.")