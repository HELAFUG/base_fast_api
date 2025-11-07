import logging
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
)
from typing import Optional
from typing import TYPE_CHECKING
from core.models import User
from core.types.user_id import UserIdType
from core.config import settings
from api.utils.mail.welcome import welcome_email
from api.utils.user.verify import verify_email, after_verify
from api.utils.password.forgot import forgot_password_email, after_reset_password

if TYPE_CHECKING:
    from fastapi import Request

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning("User %r has registered", user.id)
        await welcome_email(user)

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning("Verification requested for user %r", user.id)
        await verify_email(user, token)

    async def on_after_verify(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning("User %r has been verified", user.id)
        await after_verify(user)

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning("Forgot password requested for user %r, token %r", user.id, token)
        await forgot_password_email(user, token)

    async def on_after_reset_password(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning("Password has been reset for user %r", user.id)
        await after_reset_password(user)
