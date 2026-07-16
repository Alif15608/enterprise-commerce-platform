from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken

from .tokens import email_verification_token
from .emails import send_verification_email, send_password_reset_email

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
    send_verification_email(user)
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
    send_password_reset_email(user, token)


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