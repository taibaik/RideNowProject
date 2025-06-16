from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from redis_cache import get_from_cache, set_cache
from services.mongodb import user_collection  # 👈 MongoDB here

app = FastAPI()

class UserCreate(BaseModel):
    id: str
    name: str
    role: str

@app.post("/users")
async def create_user(user: UserCreate):
    key = f"user:{user.id}"

    # Check Redis cache
    if get_from_cache(key):
        raise HTTPException(status_code=400, detail="User already exists")

    # Check MongoDB for existing user
    existing = await user_collection.find_one({"_id": user.id})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists in DB")

    data = user.dict()
    data["_id"] = data.pop("id")

    await user_collection.insert_one(data)
    set_cache(key, data)

    return {"message": "User created", "user": data}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    key = f"user:{user_id}"
    user_data = get_from_cache(key)
    if user_data:
        return user_data

    user = await user_collection.find_one({"_id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = {
        "id": user["_id"],
        "name": user["name"],
        "role": user["role"]
    }
    set_cache(key, result)
    return result
