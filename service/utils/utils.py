from service.utils.logger import get_logger

logger = get_logger()


async def is_in_cache(cache_client, key):
    logger.debug(f"Check if item {key} in cache")
    value = await cache_client.get(key)
    return value if value is not None else False
