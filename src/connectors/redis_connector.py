import redis.asyncio as redis
import logging


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        logging.info(f"Starting Redis connection {self.host=}, {self.port=}...")
        self.redis = await redis.Redis(host=self.host, port=self.port)
        logging.info("Redis connection established")

    async def set(self, key: str, value: str, expire: int | None = None):
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key):
        return await self.redis.get(key)

    async def delete(self, key):
        await self.redis.delete(key)

    async def close(self):
        await self.redis.close()
        logging.info("Redis connection closed")
