from fastapi import Depends
from fastapi_users import BaseUserManager
from typing import Optional
from typing import TYPE_CHECKING
from core.models import User
from core.types.user_id import UserIdType
from core.config import settings
from core.models.mixins import IdIntMixin
import logging


if TYPE_CHECKING:
    from fastapi import Request

log = logging.getLogger(__name__)


class UserManager(IdIntMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(self, user: User, request: Optional["Request"] = None):
        log.warning("User %r has registered", user.id)
