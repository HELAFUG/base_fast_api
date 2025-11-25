import hashlib
from typing import Callable, Any, Tuple, Dict, Optional
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi import Request, Response
from fastapi.security import HTTPBearer
from fastapi_cache.decorator import cache
from typing import Annotated, TYPE_CHECKING
from core.config import settings
from core.schemas.user import UserRead, UserUpdate
from core.models.user import SQLAlchemyUserDatabase
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


def users_list_key_builder(
    func: Callable[..., Any],
    namespace: str,
    *,
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> str:
    exclude_types = (SQLAlchemyUserDatabase,)
    kw_cache = {}
    for name, value in kwargs.items():
        if isinstance(value, exclude_types):
            continue
        kw_cache[name] = value
    cache_key = hashlib.md5(
        f"{func.__module__}{func.__name__}{args}{kw_cache}".encode(),
    ).hexdigest()

    return f"{namespace}:{cache_key}"


@router.get("", response_model=list[UserRead])
@cache(
    expire=60,
    key_builder=users_list_key_builder,
    namespace=settings.cache.name_space.users_list,
)
async def get_all(users_db: Annotated["SQLAlchemyUserDatabase", Depends(get_users_db)]):
    users = await users_db.get_users()
    return [UserRead.model_validate(user) for user in users]


router.include_router(
    fastapi_users.get_users_router(
        user_schema=UserRead,
        user_update_schema=UserUpdate,
    )
)
