from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import HTTPBearer
from typing import Annotated, TYPE_CHECKING
from core.config import settings
from core.schemas.user import UserRead, UserUpdate
from api.dependencies.authentication.users import get_users_db
from .fastapi_users import fastapi_users

if TYPE_CHECKING:
    from core.authentication.user_manager import SQLAlchemyUserDatabase

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
    dependencies=[Depends(http_bearer)],
)


@router.get("sex", response_model=list[UserRead])
async def get_all(users_db: Annotated["SQLAlchemyUserDatabase", Depends(get_users_db)]):
    return await users_db.get_users()


router.include_router(
    fastapi_users.get_users_router(
        user_schema=UserRead,
        user_update_schema=UserUpdate,
    )
)
