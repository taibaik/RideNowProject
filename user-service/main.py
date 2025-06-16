from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from redis_cache import get_from_cache, set_cache

app = FastAPI()

class UserCreate(BaseModel):
    id: str
    name: str
    role: str

@app.post("/users")
async def create_user(user: UserCreate):
    key = f"user:{user.id}"
    if get_from_cache(key):
        raise HTTPException(status_code=400, detail="User already exists")
    set_cache(key, user.dict())
    return {"message": "User created", "user": user.dict()}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user_data = get_from_cache(f"user:{user_id}")
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data
