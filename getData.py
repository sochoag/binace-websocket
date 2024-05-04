
import asyncio
import websockets
import json
from datetime import datetime

async def connect():
  async with websockets.connect('wss://fstream.binance.com/ws/btcusdt@kline_1m') as websocket:
    await receive_data(websocket)

async def receive_data(websocket):
  try:
    while True:
      b_response=await websocket.recv()
      data = json.loads(b_response)
      # print(data)
      isClose = data['k']['x']
      time =  data['E']
      time_formatted = datetime.fromtimestamp(time/1000).strftime('%H:%M')
      if isClose:
        result = {"coin":data['s'],
                "high":data['k']['h'],
                "low":data['k']['l'],
                "open":data['k']['o'],
                "close":data['k']['c'],
                "operation":"SELL",
                "time":time_formatted}
        print(result)
  except asyncio.exceptions.CancelledError:
    print("Closing connection due to keyboard interrupt...")
    await websocket.close()

if __name__ == "__main__":
  asyncio.run(connect())