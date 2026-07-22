# tests/test_channel_layer.py
import asyncio
from channels_redis.core import RedisChannelLayer

async def test():
    layer = RedisChannelLayer(hosts=["redis://redis:6379/2"])
    await layer.send("test-channel", {"type": "test.message"})
    print("Redis channel layer send succeeded")

asyncio.run(test())