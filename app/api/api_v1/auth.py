from fastapi import APIRouter
from core.config import settings
from api.dependencies.authentication import authentication_backend
from core.schemas.user import UserRead, UserCreate
from .fastapi_users import fastapi_users


router = APIRouter(
    prefix=settings.api.v1.auth,
)

router.include_router(
    router=fastapi_users.get_register_router(
        user_create_schema=UserCreate,
        user_schema=UserRead,
    )
)

router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
    )
)
