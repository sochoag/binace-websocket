import asyncio
import websockets
import time
import json
values= {
  "coin":"BTCUSDT",
  "high":1000,
  "low":500,
  "open": 530,
  "close": 800,
  "operation":"BUY/SELL",
  "time": "HH:MM"
}
async def publish_data(websocket, payload):
    while True :
        response= json.dumps(payload)
        await websocket.send(response)
        print(response)
        await asyncio.sleep(1)

if __name__ == "__main__":
  start_server = websockets.serve(publish_data, "localhost", 8000)

  asyncio.get_event_loop().run_until_complete(start_server)
  asyncio.get_event_loop().run_forever()