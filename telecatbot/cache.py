import redis

from .config import CACHE_CONFIG


cache = redis.StrictRedis(**CACHE_CONFIG)
