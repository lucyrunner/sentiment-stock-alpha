import redis
from src.config import REDIS_URL

def get_redis() -> redis.Redis:
    return redis.from_url(REDIS_URL, decode_responses=True)
