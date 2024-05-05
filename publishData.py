import json 
import asyncio
import time
from pymongo import MongoClient
from mongoconection import MONGO_URI, MONGO_DATABASE, MONGO_COLLECTION

client = MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]
collection = db[MONGO_COLLECTION]

async def publish_data(websocket, payload):
    response = json.dumps(payload)
    await websocket.send(response)
    print("response sent:", response)

    try:
        while True: 
          # Save data to MongoDB
          collection.insert_one(payload)
          print(" ✅✅✅✅ Data saved to MongoDB successfully! ✅✅✅")
          await asyncio.sleep(0.1)  # Wait for 10 seconds
    except Exception as e:
        print(f"Error saving data to MongoDB: {e}")
        client.close()

if __name__ == "__publish_data__":
  asyncio.run(publish_data())
