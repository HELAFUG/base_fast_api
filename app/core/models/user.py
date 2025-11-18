from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.orm import Mapped, relationship

from typing import TYPE_CHECKING
from .mixins import IdIntMixin
from .base import Base
from core.types.user_id import UserIdType

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from .access_token import AccessToken


class User(Base, IdIntMixin, SQLAlchemyBaseUserTable[UserIdType]):
    access_tokens: Mapped[list["AccessToken"]] = relationship(
        back_populates="user",
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)

    def __str__(self):
        return self.email
