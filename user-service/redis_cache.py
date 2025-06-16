import redis
import json

redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)
CACHE_TTL = 300  # 5 minutes

def get_from_cache(key: str):
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None

def set_cache(key: str, value: dict, ttl: int = CACHE_TTL):
    redis_client.set(key, json.dumps(value), ex=ttl)
