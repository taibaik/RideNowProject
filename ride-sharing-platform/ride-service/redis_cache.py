# redis_cache.py

import redis
import json

# ✅ Correct host for Docker Compose (matches service name in docker-compose.yml)
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

# How long to keep cache (in seconds)
CACHE_TTL = 300  # 5 minutes

def get_from_cache(key: str):
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None

def set_cache(key: str, value: dict, ttl: int = CACHE_TTL):
    print(f"SET CACHE: {key} = {value}")  # optional debug print
    redis_client.set(key, json.dumps(value), ex=ttl)
