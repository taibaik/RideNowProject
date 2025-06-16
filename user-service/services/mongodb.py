# user-service/services/mongodb.py

from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["ride_now"]  # You can rename this DB name if needed
user_collection = db["users"]
