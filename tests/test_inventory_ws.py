import asyncio
import websockets

async def main():
    uri = "ws://localhost/ws/inventory/1/"   # replace 1 with a real product id
    async with websockets.connect(uri) as ws:
        print("Connected. Waiting for stock updates... (update the product in another terminal)")
        while True:
            message = await ws.recv()
            print("Received:", message)

asyncio.run(main())