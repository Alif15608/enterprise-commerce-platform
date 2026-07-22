from django.urls import re_path
from .consumers import InventoryConsumer

websocket_urlpatterns = [
    re_path(r"ws/inventory/(?P<product_id>\d+)/$", InventoryConsumer.as_asgi()),
]