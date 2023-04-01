async def is_search_in_cache(cache_client, key):
    value = await cache_client.get(key)
    return value if value is not None else False
