import redis
from app.core.config import settings

# Create Redis connection
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
    decode_responses=True
)

def get_redis_client():
    return redis_client