from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.asyncio import Redis
from contextlib import asynccontextmanager
from core.config import settings
from core.models import db_helper
from core import broker
from api import router
import logging

logging.basicConfig(format=settings.logging.log_format)


@asynccontextmanager
async def lifespan(app):
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db.cache,
    )
    FastAPICache.init(
        RedisBackend(redis),
        prefix=settings.cache.prefix,
    )
    if not broker.is_worker_process:
        await broker.startup()
    yield
    await db_helper.dispose()
    if not broker.is_worker_process:
        await broker.shutdown()


main_app = FastAPI(lifespan=lifespan)

main_app.include_router(router=router)
