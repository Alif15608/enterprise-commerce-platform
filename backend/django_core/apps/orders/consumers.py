from channels.generic.websocket import AsyncJsonWebsocketConsumer


class OrderStatusConsumer(AsyncJsonWebsocketConsumer):
    """
    Authenticated only — a customer should only ever receive status
    updates for their OWN orders, never anyone else's.
    """
    async def connect(self):
        user = self.scope["user"]
        if not user or not user.is_authenticated:
            await self.close(code=4001)
            return

        self.group_name = f"orders_user_{user.id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def order_status_update(self, event):
        await self.send_json({
            "order_number": event["order_number"],
            "status": event["status"],
        })