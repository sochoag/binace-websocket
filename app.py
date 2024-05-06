# Import necessary libraries

import asyncio
import websockets
import os
from publishData import *
from getData import get_data

# Funtion to upload data to Mongo on every new close on binance
async def upload_data():
  # WebSocket endpoint to retreive all the data from:
  # - BTCUSDT
  # - BNBUSDT
  # - ETHUSDT
  # - SOLUSDT
  # - XRPUSDT
  URI = 'wss://fstream.binance.com/stream?streams=btcusdt@kline_1m/bnbusdt@kline_1m/ethusdt@kline_1m/solusdt@kline_1m/xrpusdt@kline_1m'

  # Connection to Binance Socket
  binance_socket = await websockets.connect(URI)
  try:  
    while True:
      # Read the data
      data = await get_data(binance_socket)
      # If the new value is a close stock then process
      if data:
        # Insert the data into Mongo DataBase
        coin = await insert_data(data)
        # Log for confirmation
        print("Inserting data into: "+coin)
  except:
    # If something happens, handle the exception and retry
    print("Error with Binance connection")
  finally:
    # Close the connection 
    await binance_socket.close()


# Function to handle the connection on Railway
async def handler(websocket):
  # Variable witch stores all the coin names
  coins = ['BTCUSDT', 'BNBUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT']
  try:
    while True:
        # Iterate through each coin
        for coin in coins:
          # Retrieve the last 10 records for each coin
          response = await get_last_ten_records(coin)
          # Send the last 10 records from Mongo to the Websocket Connection
          await publish_data(websocket, response)
        # Wait 60 seconds before send the response again
        await asyncio.sleep(60)
  except websockets.exceptions.ConnectionClosedOK:
    # Handle execption when there is no client connected.
    print("No clients connected. Waiting for connections...")

# Function which start the server on RailWays
async def start_server():
    # Port for deployment injected by env variables
    port = int(os.environ.get("PORT", 8000))
    try:
      print("WebSocket server started. Waiting for connections...")
      # Start to serve
      async with websockets.serve(handler, '0.0.0.0', port):
          await asyncio.Future()
    except:
      # Handling the execption
      print("Server shutting down...")


# Main function
async def main():
  # Creating a task for start the server
  server_task = asyncio.create_task(start_server())
  # Creating a task for upload new records
  data_task = asyncio.create_task(upload_data())
  # Gathering the tasks
  try:
    await asyncio.gather(data_task, server_task)
  except:
    # Handling the execption
    print("Terminating tasks...")


if __name__ == "__main__":
    # Running the app
    asyncio.run(main())