import asyncio
import websockets

from publishData import publish_data
from getData import receive_data


import json
from datetime import datetime

async def receive_and_publish_data():
    async with  websockets.connect('wss://fstream.binance.com/ws/btcusdt@kline_1m') as binance_socket, \
                websockets.serve(publish_data, "localhost", 8000) as local_server:
        
        async with local_server:
            binance_task = asyncio.create_task(receive_data(binance_socket))
            local_task = asyncio.create_task(local_server.wait_closed())

            # Await both tasks concurrently, handling potential cancellation
            await asyncio.gather(binance_task, local_task, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(receive_and_publish_data())
