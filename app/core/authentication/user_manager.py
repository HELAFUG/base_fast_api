import logging
from typing import TYPE_CHECKING
from typing import Optional
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
)
from fastapi_cache import FastAPICache
from core.models import User
from core.types.user_id import UserIdType
from core.config import settings
from tasks import (
    welcome_email_notification,
    send_after_forgot,
    send_after_reset,
    send_after_login,
    send_after_verify_req,
    on_after_success,
)


if TYPE_CHECKING:
    from fastapi import Request
    from fastapi import Response
    from fastapi import BackgroundTasks

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    def __init__(
        self,
        user_db,
        password_hasher=None,
        background_tasks: Optional["BackgroundTasks"] = None,
    ):
        super().__init__(user_db, password_hasher)
        self.background_tasks = background_tasks

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
        back_tasks: Optional["BackgroundTasks"] = None,
    ):

        log.warning("User registered %r", user.id)
        await welcome_email_notification.kiq(user.id)

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning("Verification requested for user %r, token %r", user.id, token)
        await send_after_verify_req.kiq(user.id, token)

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning("Forgot password requested for user %r", user.id)
        await send_after_forgot.kiq(user.id, token)

    async def on_after_reset_password(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning("Reset password requested for user %r", user.id)
        await send_after_reset.kiq(user.id)

    async def on_after_verify(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning("Verification requested for user %r", user.id)
        await on_after_success.kiq(user.id)

    async def on_after_login(
        self,
        user: User,
        request: Optional["Request"] = None,
        response: Optional["Response"] = None,
    ):
        log.warning("Login requested for user %r", user.id)
        await send_after_login.kiq(user.id)
