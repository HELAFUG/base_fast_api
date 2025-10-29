from fastapi import APIRouter
from core.config import settings
from .api_v1 import api_v1_router

router = APIRouter(
    prefix=settings.api.pretix,
)

router.include_router(router=api_v1_router)
