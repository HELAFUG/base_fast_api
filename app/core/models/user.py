from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase as SQLAlchemyUserDatabaseGeneric,
)
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy import select
from typing import TYPE_CHECKING
from .mixins import IdIntMixin
from .base import Base
from core.types.user_id import UserIdType

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from .access_token import AccessToken
    from .user import User


class SQLAlchemyUserDatabase(SQLAlchemyUserDatabaseGeneric):
    async def get_users(self) -> list["User"]:
        stmt = select(User).order_by(User.id)
        res = await self.session.scalars(stmt)
        return list(res.all())


class User(Base, IdIntMixin, SQLAlchemyBaseUserTable[UserIdType]):
    access_tokens: Mapped[list["AccessToken"]] = relationship(
        back_populates="user",
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)

    def __str__(self):
        return self.email
