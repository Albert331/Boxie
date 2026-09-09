import asyncio
from websockets.asyncio.client import connect

async def receive_loop(ws):
    async for message in ws:
        print(f"\n[Received] {message}")

async def send_loop(ws):
    while True:
        msg = await asyncio.to_thread(input, "Send: ")
        await ws.send(msg)

async def main():
    async with connect("ws://localhost:8001") as ws:
        await asyncio.gather(receive_loop(ws), send_loop(ws))

asyncio.run(main())