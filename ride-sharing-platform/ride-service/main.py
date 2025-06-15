from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from redis_cache import get_from_cache, set_cache
from services.mongodb import ride_collection

app = FastAPI()

class RideCreate(BaseModel):
    id: str
    driver: str
    status: str

@app.post("/rides")
async def create_ride(ride: RideCreate):
    existing = await ride_collection.find_one({"_id": ride.id})
    if existing:
        raise HTTPException(status_code=400, detail="Ride already exists")

    data = ride.dict()
    data["_id"] = data.pop("id")
    await ride_collection.insert_one(data)
    set_cache(f"ride:{data['_id']}", {"id": data["_id"], **data})
    return {"message": "Ride created", "ride": {"id": data["_id"], **data}}

@app.get("/rides/{ride_id}")
async def get_ride(ride_id: str):
    cache_key = f"ride:{ride_id}"
    ride = get_from_cache(cache_key)
    if ride:
        print(f"Ride Cache HIT: {cache_key}")
        return ride

    ride = await ride_collection.find_one({"_id": ride_id})
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")

    result = {"id": ride["_id"], "driver": ride["driver"], "status": ride["status"]}
    set_cache(cache_key, result)
    return result
