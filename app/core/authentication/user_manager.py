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
from tasks import (
    welcome_email_notification,
    send_after_forgot,
    send_after_reset,
)
from mailing.passwords.forgot import send_password_forgot_email
from mailing.passwords.reset import send_reset_password_email
from mailing.user.verify import (
    send_verify_email,
    send_success_email,
)
from mailing.user.login import send_login_email


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
        await welcome_email_notification.kiq(user.id)

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
        await send_after_forgot.kiq(user.id, token)

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
