from os import getenv

TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')
THECATAPI_KEY = getenv('THECATAPI_KEY')

CACHE_CONFIG = dict(
    host=getenv('REDIS_HOST', 'localhost'),
    port=getenv('REDIS_PORT', 6379),
    db=getenv('REDIS_DB', 0)
)