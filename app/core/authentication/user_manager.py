import logging
from typing import TYPE_CHECKING
from typing import Optional
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
)
from core.models import User
from core.types.user_id import UserIdType
from core.config import settings
from api.utils.mail import send_welcome_email
from api.utils.passwords.forgot import send_password_forgot_email
from api.utils.passwords.reset import send_reset_password_email
from api.utils.user.verify import (
    send_verify_email,
    send_success_email,
)
from api.utils.user.login import send_login_email


if TYPE_CHECKING:
    from fastapi import Request
    from fastapi import Response

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning("User registered %r", user.id)
        await send_welcome_email(user)

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning("Verification requested for user %r, token %r", user.id, token)
        await send_verify_email(user=user, token=token)

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional["Request"] = None,
    ):
        log.warning("Forgot password requested for user %r", user.id)
        await send_password_forgot_email(user=user, token=token)

    async def on_after_reset_password(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning("Reset password requested for user %r", user.id)
        await send_reset_password_email(user=user)

    async def on_after_verify(
        self,
        user: User,
        request: Optional["Request"] = None,
    ):
        log.warning("Verification requested for user %r", user.id)
        await send_success_email(user=user)

    async def on_after_login(
        self,
        user: User,
        request: Optional["Request"] = None,
        response: Optional["Response"] = None,
    ):
        log.warning("Login requested for user %r", user.id)
        await send_login_email(user=user)
