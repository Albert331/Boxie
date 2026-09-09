import asyncio
import json
import random
from websockets.asyncio.server import serve

async def send_loop(websocket):
    while True:
        await websocket.send(json.dumps({"type": "punch"}))
        print("Sent automated punch")
        await asyncio.sleep(3)

async def receive_loop(websocket):
    async for message in websocket:
        print(f"Got: {message}")

async def handler(websocket):
    await asyncio.gather(send_loop(websocket), receive_loop(websocket))

async def main():
    async with serve(handler, "localhost", 8001) as server:
        print("Server running on ws://localhost:8001")
        await server.serve_forever()

asyncio.run(main())