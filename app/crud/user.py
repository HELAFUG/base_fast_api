from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import User


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return (await session.execute(stmt)).scalars().first()
