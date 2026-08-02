# ruff: noqa: E402, I001
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from apps.core.ws_auth import JWTAuthMiddleware
from config.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(URLRouter(websocket_urlpatterns)),
})
