import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from src.utils.globals import globals_instance

load_dotenv()

# MongoDB connection setup
client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client["gtr-pi"]
collection = db["gtr-pi-events"]

async def poll_mongo():
    while True:
        events = await collection.find().to_list(None)
        for event in events:
            globals_instance.event_queue.put(event)
            await collection.delete_one({"_id": event["_id"]})
        await asyncio.sleep(1)  # Poll every second