from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    """
    Generates single-use, time-limited tokens for email verification.
    Reuses Django's built-in HMAC scheme (tied to user state) rather than
    a separate reset generator, but with a distinct salt so a verification
    token can never accidentally be replayed as a password reset token.
    """
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"


email_verification_token = EmailVerificationTokenGenerator()