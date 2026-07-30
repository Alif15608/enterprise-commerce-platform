from .base import *  # noqa: F401,F403

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "daphne", "django", "nginx"]

CORS_ALLOW_ALL_ORIGINS = True

LOGGING["root"]["level"] = "DEBUG"

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "x-guest-token",   # our custom header — must be explicitly allowlisted
]
