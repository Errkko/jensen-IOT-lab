import json
import os
import redis

client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", "6379")),
    decode_responses=True,
)


def get_latest_from_cache(device_id):
    # TODO M2: 
    # Läs senaste mätvärdet från Redis.
    key = client.get(f"latest:{device_id}")
    if key:
        return json.loads(key)
    return None


def set_latest_in_cache(device_id, measurement):
    # TODO M2: 
    # Spara senaste mätvärdet i Redis.
    key = client.get(f"latest:{device_id}")
    client.set(f"latest:{device_id}", json.dumps(measurement))