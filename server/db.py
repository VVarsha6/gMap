import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.donations

async def connect_to_mongo():
    try:
        # Just a simple command to confirm connection
        await client.admin.command("ping")
        await db.locations.create_index([("coordinates", "2dsphere")])
        print("✅ Connected to MongoDB!")
    except Exception as e:
        print("❌ MongoDB connection failed:", e)