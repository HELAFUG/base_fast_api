from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.config import settings
from core.models import db_helper
from api import router
import logging

logging.basicConfig(format=settings.logging.log_format)


@asynccontextmanager
async def lifespan(app):
    yield
    await db_helper.dispose()


main_app = FastAPI(lifespan=lifespan)

main_app.include_router(router=router)
