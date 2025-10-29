from fastapi import APIRouter
from core.config import settings
from .auth import router as auth_router

api_v1_router = APIRouter(
    prefix=settings.api.v1.prefix,
    tags=["V1"],
)

api_v1_router.include_router(router=auth_router)
