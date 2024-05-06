
import asyncio
import websockets
import json
from datetime import datetime, timezone, timedelta

# Global variable to store the last value of each coin
last_price = [None,None,None,None,None]

# Function to get data from Binance
async def get_data(websocket):
  global last_price

  # Getting the binance data
  b_response=await websocket.recv()
  # Converting data into a dictionary
  data = json.loads(b_response)
  
  # Creating a boolean variable to check if the transaction is close
  isClose = data['data']['k']['x']
  
  # If is close
  if isClose:
    # Create a timestamp
    time =  data['data']['E']

    # Creating a timezone offset
    GTM5 = timezone(timedelta(hours=-5))

    # Fomating the time as HH:MM
    time_formatted = datetime.fromtimestamp(time/1000, tz=GTM5).strftime('%H:%M')

    # Getting the current price
    price = float(data['data']['k']['c'])

    # Variable with coins names
    coins = ['BTCUSDT', 'BNBUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT']

    # Index of each coin
    index = coins.index(data['data']['s'])

    # Checking if price is None
    if last_price[index] is not None:
      # Asign SELL or BUY value to operation
      if last_price[index] > price:
        operation = "SELL"
      else:
        operation = "BUY"
    else:
      operation = "SELL"

    # Populating las price
    last_price[index] = price

    # Populatin response
    result = {"coin":data['data']['s'],
            "high":data['data']['k']['h'],
            "low":data['data']['k']['l'],
            "open":data['data']['k']['o'],
            "close":data['data']['k']['c'],
            "operation":operation,
            "time":time_formatted}
    
    # Returning response
    return result