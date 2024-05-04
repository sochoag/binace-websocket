import asyncio
import websockets

from publishData import publish_data
from getData import get_data

async def receive_and_publish_data(websocket):
    async with  websockets.connect('wss://fstream.binance.com/ws/btcusdt@kline_1m') as binance_socket:
          while True:
            data = await get_data(binance_socket)
            if data:
              try:
                await publish_data(websocket, data)
              except websockets.exceptions.ConnectionClosedOK:
                print("No clients connected. Waiting for connections...")
                break
async def start_server():
    try:
      print("WebSocket server started. Waiting for connections...")
      async with websockets.serve(receive_and_publish_data, 'localhost', 8000):
          await asyncio.Future()
    except:
      print("Server shutting down...")

if __name__ == "__main__":
    asyncio.run(start_server())
