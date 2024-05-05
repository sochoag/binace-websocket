from pymongo.mongo_client import MongoClient
import asyncio
import time

# # Replace with your MongoDB connection details
MONGO_URI = "mongodb+srv://sgcriollogal:X4eT0zmCCoZ1cnog@practica.xrlm29s.mongodb.net/?retryWrites=true&w=majority&appName=Practica"
MONGO_DATABASE = "CryptoInfo"
MONGO_COLLECTION = "Coins"

async def save_data_to_mongo(data,collection):
    """Saves data to a MongoDB collection."""
    try:
        collection.insert_one(data)
        print("😎 Data saved to MongoDB successfully!")
    except Exception as e:
        print(f"Error saving data to MongoDB: {e}")
       
async def main():
    """Continuously sends data to MongoDB every 10 seconds."""
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]
    collection = db[MONGO_COLLECTION]
    
    while True:
        try:
            # Replace with your logic to generate data (e.g., API call, sensor reading)
            result = {"coin": '123',  # Replace with actual data generation
                    "high": 'gei',
                    "low": 'david',
                    "open": 'sara',
                    "close": 'holamundo',
                    "operation": "nose",
                    "time": time.strftime('%H:%M:%S')}

            await save_data_to_mongo(result,collection)
        # await asyncio.sleep(0.1)  # Wait for 10 seconds
        except:
            print ("😒 Cerrando conexión")
            client.close()  # Ensure connection is closed


if __name__ == "__main__":
    asyncio.run(main())