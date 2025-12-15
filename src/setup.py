from src.connectors.redis_manager import RedisManager
from src.config import settings

redis_manager = RedisManager(
    host=settings.CACHE_HOST,
    port=settings.CACHE_PORT
)