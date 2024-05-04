import asyncio
import websockets
import time
import json
payLoad= {
  "coin":"BTCUSDT",
  "high":1000,
  "low":500,
  "open": 530,
  "close": 800,
  "operation":"BUY/SELL",
  "time": "HH:MM"
}
async def handler(websocket):
    while True :
        response= json.dumps(payLoad)
        await websocket.send(response)
        print(response)
        await asyncio.sleep(1)

start_server = websockets.serve(handler, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()