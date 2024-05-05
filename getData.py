
import asyncio
import websockets
import json
from datetime import datetime

last_price = [None,None,None,None,None]

async def connect():
  async with websockets.connect('wss://fstream.binance.com/stream?streams=btcusdt@kline_1m/bnbusdt@kline_1m/ethusdt@kline_1m/solusdt@kline_1m/xrpusdt@kline_1m') as websocket:
    await get_data(websocket)

async def get_data(websocket):
  global last_price

  b_response=await websocket.recv()
  data = json.loads(b_response)
  
  isClose = data['data']['k']['x']
  
  if isClose:

    time =  data['data']['E']
    time_formatted = datetime.fromtimestamp(time/1000).strftime('%H:%M')

    price = float(data['data']['k']['c'])

    match data['data']['s']:
      case "BTCUSDT":
        index = 0
      case "BNBUSDT":
        index = 1
      case "ETHUSDT":
        index = 2
      case "SOLUSDT":
        index = 3
      case "XRPUSDT":
        index = 4

    if last_price[index] is not None:
      if last_price[index] > price:
        operation = "SELL"
      else:
        operation = "BUY"
    else:
      operation = None

    last_price[index] = price

    result = {"coin":data['data']['s'],
            "high":data['data']['k']['h'],
            "low":data['data']['k']['l'],
            "open":data['data']['k']['o'],
            "close":data['data']['k']['c'],
            "operation":operation,
            "time":time_formatted}
    return result

if __name__ == "__main__":
  asyncio.run(connect())