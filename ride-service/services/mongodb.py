# services/mongodb.py
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["ride_sharing"]
ride_collection = db["rides"]
