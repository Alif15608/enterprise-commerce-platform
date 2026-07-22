from channels.generic.websocket import AsyncJsonWebsocketConsumer


class InventoryConsumer(AsyncJsonWebsocketConsumer):
    """
    Public, unauthenticated — anyone viewing a product page can watch its
    stock level update live. No sensitive data here, so no auth required,
    unlike OrderStatusConsumer below.
    """
    async def connect(self):
        self.product_id = self.scope["url_route"]["kwargs"]["product_id"]
        self.group_name = f"inventory_{self.product_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def inventory_update(self, event):
        """
        Handler name matches the 'type' field sent from the signal
        (see catalog/signals.py) — Channels routes group_send messages
        to a method named after their 'type', with dots replaced by underscores.
        """
        await self.send_json({
            "product_id": event["product_id"],
            "stock_quantity": event["stock_quantity"],
        })