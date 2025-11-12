from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.config import settings
from core.models import db_helper
from core import broker
from api import router
import logging

logging.basicConfig(format=settings.logging.log_format)


@asynccontextmanager
async def lifespan(app):
    await broker.startup()
    yield
    await db_helper.dispose()
    await broker.shutdown()


main_app = FastAPI(lifespan=lifespan)

main_app.include_router(router=router)
