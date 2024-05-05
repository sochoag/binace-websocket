import json 
import asyncio
import time
from pymongo import MongoClient, DESCENDING
from mongoconection import MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION

client = MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]
collection = db[MONGO_COLLECTION]

async def insert_data(payload):
  try:
    collection.insert_one(payload)
    # print(" ✅✅✅✅ Data saved to MongoDB successfully! ✅✅✅")
    return payload['coin']
  except Exception as e:
    print(f"Error saving data to MongoDB: {e}")
    client.close()

async def get_last_ten_records(coin):  
  try:
    response = {}
    response['coin'] = coin
    response["values"] = []
    response["operations"] = []
    response["time"] = []

    registers = collection.find({"coin":f"{coin}"}).sort({'$natural':-1}).limit(10)

    for register in registers:
      
      response["values"].append(register["close"])
      response["operations"].append(register["operation"])
      response['time'].append(register["time"])

    return response
  
  except Exception as e:
    print(f"Cant find registers {e}")


async def publish_data(websocket, payload):
    response = json.dumps(payload)
    await websocket.send(response)
    print("-------------------------------------------")
    print(response)
    print("-------------------------------------------")

if __name__ == "__publish_data__":
  asyncio.run(publish_data())
