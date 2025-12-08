import asyncio
import contextlib

from os import getenv
from api.dependencies.authentication import get_users_db
from api.dependencies.authentication import get_user_manager
from core.models import User
from core.authentication.user_manager import UserManager
from core.schemas.user import UserCreate
from core.models import db_helper
from tasks import welcome_email_notification

get_users_db_context = contextlib.asynccontextmanager(get_users_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


default_email = getenv("ADMIN_EMAIL", "admin@example.com")
default_password = getenv("ADMIN_PASSWORD", "password")
default_is_active = True
default_is_superuser = True
default_is_verified = True


async def create_user(user_manager: UserManager, user: UserCreate) -> User:
    user = await user_manager.create(
        user_create=user,
        safe=False,
    )
    return user


async def create_superuser(
    email: str = default_email,
    password: str = default_password,
    is_active: bool = default_is_active,
    is_superuser: bool = default_is_superuser,
    is_verified: bool = default_is_verified,
):
    user_create = UserCreate(
        email=email,
        password=password,
        is_active=is_active,
        is_superuser=is_superuser,
        is_verified=is_verified,
    )

    async with db_helper.session_factory() as session:
        async with get_users_db_context(session) as users_db:
            async with get_user_manager_context(users_db) as user_manager:
                await welcome_email_notification.kiq(user_create.id)
                return await create_user(user_manager, user_create)


if __name__ == "__main__":
    asyncio.run(create_superuser())
