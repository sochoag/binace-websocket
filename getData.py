
import asyncio
import websockets
import json
from datetime import datetime

async def connect():
  async with websockets.connect('wss://fstream.binance.com/ws/btcusdt@kline_1m') as websocket:
    await get_data(websocket)

async def get_data(websocket):
  b_response=await websocket.recv()
  data = json.loads(b_response)
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
    return result

if __name__ == "__main__":
  asyncio.run(connect())