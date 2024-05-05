import asyncio
import websockets
import os

from publishData import publish_data
from getData import get_data

async def receive_and_publish_data(websocket):
    async with  websockets.connect('wss://fstream.binance.com/stream?streams=btcusdt@kline_1m/bnbusdt@kline_1m/ethusdt@kline_1m/solusdt@kline_1m/xrpusdt@kline_1m') as binance_socket:
          while True:
            data = await get_data(binance_socket)
            if data:
              try:
                await publish_data(websocket, data)
              except websockets.exceptions.ConnectionClosedOK:
                print("No clients connected. Waiting for connections...")
                break
async def start_server():
    port = int(os.environ.get("PORT", 8000))
    try:
      print("WebSocket server started. Waiting for connections...")
      async with websockets.serve(receive_and_publish_data, '0.0.0.0', port):
          await asyncio.Future()
    except:
      print("Server shutting down...")

if __name__ == "__main__":
    asyncio.run(start_server())
