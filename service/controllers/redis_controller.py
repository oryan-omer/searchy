import base64
import json

import aioredis as aioredis

from service.controllers.base import BaseGracefulShutdown
from service.utils.logger import get_logger
from service.utils.settings import settings

logger = get_logger()


class RedisController(BaseGracefulShutdown):
    _instance = None

    def __init__(self):
        self.redis_client = None

    async def init_async_client(self, redis_host=settings.REDIS_URL):
        logger.info("starting redis server..")
        self.redis_client = await aioredis.from_url(redis_host)
        return self

    @classmethod
    async def get_instance(cls):
        if cls._instance is None:
            cls._instance = RedisController()
            await cls._instance.init_async_client()

        return cls._instance

    async def set(self, key: str, value):
        try:
            logger.debug(f"set key in cache, key={key}")
            await self.redis_client.set(key, json.dumps(value))
        except Exception as e:
            logger.error(f"Error setting key in cache store, key={key}, error={e}")

    async def get(self, key: str):
        try:
            logger.debug(f"get key from cache, key={key}")
            bin_value = await self.redis_client.get(key)
            return json.loads(bin_value.decode("utf8")) if bin_value is not None else bin_value
        except Exception as e:
            logger.error(f"Error getting key from cache store, key={key}, error={e}")
            raise Exception(f"Error getting key from cache store, key={key}, error={e}")

    async def shutdown(self):
        logger.info("shutdown redis client")
        await self.redis_client.close()


async def get_redis_controller():
    return await RedisController.get_instance()
