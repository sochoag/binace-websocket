import asyncio
import websockets
import os
from publishData import *
from getData import get_data

async def upload_data():
  binance_socket = await websockets.connect('wss://fstream.binance.com/stream?streams=btcusdt@kline_1m/bnbusdt@kline_1m/ethusdt@kline_1m/solusdt@kline_1m/xrpusdt@kline_1m')
  while True:
    try:  
      data = await get_data(binance_socket)
      if data:
        coin = await insert_data(data)
        print("Inserting data into"+coin)
    except:
      print("Error with Binance connection")
    finally:
      await binance_socket.close()

async def handler(websocket):
  coins = ['BTCUSDT', 'BNBUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT']
  try:
    while True:
        for coin in coins:
          response = await get_last_ten_records(coin)
          await publish_data(websocket, response)
        await asyncio.sleep(60)
  except websockets.exceptions.ConnectionClosedOK:
    print("No clients connected. Waiting for connections...")


async def start_server():
    port = int(os.environ.get("PORT", 8000))
    try:
      print("WebSocket server started. Waiting for connections...")
      async with websockets.serve(handler, '0.0.0.0', port):
          await asyncio.Future()
    except:
      print("Server shutting down...")


async def main():
  server_task = asyncio.create_task(start_server())
  data_task = asyncio.create_task(upload_data())
  await asyncio.gather(data_task, server_task)

if __name__ == "__main__":
    asyncio.run(main())