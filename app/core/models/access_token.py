from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenTable,
    SQLAlchemyBaseAccessTokenTable,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey
from typing import TYPE_CHECKING
from core.types.user_id import UserIdType
from .base import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable):
    user_id: Mapped[UserIdType] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyAccessTokenTable(session, cls)
