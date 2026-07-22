import asyncio
import websockets

async def main():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg0NzA3NjU0LCJpYXQiOjE3ODQ3MDY3NTQsImp0aSI6ImQ2Y2VmOGUxM2Q0ODRhMDM5NWNhOWQxNmI1OTFkNGFkIiwidXNlcl9pZCI6Mn0.VcyPvzXiv-Ui5-CMjVHJlnG8NpVuRip-fh1cAYm8U4E"
    uri = f"ws://localhost/ws/orders/?token={token}"
    async with websockets.connect(uri) as ws:
        print("Connected as authenticated user. Waiting for order status updates...")
        while True:
            message = await ws.recv()
            print("Received:", message)

asyncio.run(main())