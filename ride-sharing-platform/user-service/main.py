from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from redis import Redis
import json

app = FastAPI()
redis_client = Redis(host="redis", port=6379, decode_responses=True)

class UserCreate(BaseModel):
    id: str
    name: str
    role: str

@app.post("/users")
async def create_user(user: UserCreate):
    key = f"user:{user.id}"
    if redis_client.exists(key):
        raise HTTPException(status_code=400, detail="User already exists")
    redis_client.set(key, json.dumps(user.dict()))
    return {"message": "User created", "user": user.dict()}

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    key = f"user:{user_id}"
    data = redis_client.get(key)
    if not data:
        raise HTTPException(status_code=404, detail="User not found")
    return json.loads(data)
