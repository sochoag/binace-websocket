import asyncio
import websockets
import os
from publishData import *
from getData import get_data
import json

async def receive_and_publish_data(websocket, path):
    print(path)
    if path == "/":

      coins = ['BTCUSDT', 'BNBUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT']

      for coin in coins:
        response = await get_last_ten_records(coin)
        await publish_data(websocket, response)

      async with  websockets.connect('wss://fstream.binance.com/stream?streams=btcusdt@kline_1m/bnbusdt@kline_1m/ethusdt@kline_1m/solusdt@kline_1m/xrpusdt@kline_1m') as binance_socket:
          try:
            while True:
              data = await get_data(binance_socket)
              if data:
                coin = await insert_data(data)
                response = await get_last_ten_records(coin)
                await publish_data(websocket, response)
          except websockets.exceptions.ConnectionClosedOK:
            print("No clients connected. Waiting for connections...")
            
    if path == "/BTCUSDT":
      response = await get_last_ten_records()
      await publish_data(websocket, response)


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
