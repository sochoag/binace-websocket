import json 
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Creating the Mongo client
client = MongoClient(os.getenv("MONGO_URI"))
# Accessing to Mongo DataBase
db = client[os.environ.get("MONGO_DATABASE")]
# Accessing to Mongo Collection
collection = db[os.environ.get("MONGO_COLLECTION")]

# Function to insert data into Mongo
async def insert_data(payload):
  try:
    # Inserting the payload
    collection.insert_one(payload)
    # Returning the coin name
    return payload['coin']
  # Handling exception
  except Exception as e:
    print(f"Error saving data to MongoDB: {e}")
    # In something happens the client get close
    client.close()

# Function to get last 10 records from Mongo
async def get_last_ten_records(coin):  
  try:
    # Preparing response variable
    response = {}
    response['coin'] = coin
    response["values"] = []
    response["operations"] = []
    response["time"] = []

    # Making the query
    registers = collection.find({"coin":f"{coin}"}).sort({'$natural':-1}).limit(10)

    for register in registers:
      response["values"].append(register["close"])
      response["operations"].append(register["operation"])
      response['time'].append(register["time"])

    # Returning response
    return response

  # Handling exception  
  except Exception as e:
    print(f"Cant find registers {e}")

# Function to publis data to Websocket
async def publish_data(websocket, payload):
    # Convert payload dictionary into json 
    response = json.dumps(payload)
    # Send the response
    await websocket.send(response)
    # Print confirmation
    print("-------------------------------------------")
    print("Response:"+response)
    print("-------------------------------------------")
