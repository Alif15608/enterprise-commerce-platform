from django.urls import re_path

from apps.catalog.routing import websocket_urlpatterns as catalog_ws
from apps.orders.routing import websocket_urlpatterns as orders_ws

websocket_urlpatterns = catalog_ws + orders_ws