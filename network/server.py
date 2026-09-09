import asyncio
import json
import random
from websockets.asyncio.server import serve

connections = []  

async def handler(websocket):
    connections.append(websocket)
    print(f"Player connected ({len(connections)}/2)")

    try:
        async for message in websocket:
            for peer in connections:
                if peer != websocket:
                    await peer.send(message)
    finally:
        connections.remove(websocket)
        print(f"Player disconnected ({len(connections)}/2)")



async def main():
    async with serve(handler, "", 8001) as server:
        print("Server running on ws://localhost:8001")
        await server.serve_forever()

asyncio.run(main())