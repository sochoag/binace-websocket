import asyncio
import websockets

from publishData import publish_data
from getData import get_data

async def receive_and_publish_data(websocket):
    async with  websockets.connect('wss://fstream.binance.com/ws/btcusdt@kline_1m') as binance_socket:
          while True:
            valores = await get_data(binance_socket)
            if valores:
              print(valores)
              # await websocket.send(json.dumps(valores))
              await publish_data(websocket, valores)

async def start_server():
    async with websockets.serve(receive_and_publish_data, 'localhost', 8000):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(start_server())
