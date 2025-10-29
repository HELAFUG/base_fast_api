from fastapi import FastAPI
from contextlib import asynccontextmanager
from core.config import settings
from core.models import db_helper
import uvicorn


@asynccontextmanager
async def lifespan(app):
    yield
    await db_helper.dispose


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        host=settings.srv.host,
        port=settings.srv.port,
    )
