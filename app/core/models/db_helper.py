from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator
from core.config import settings


class DBHelper:
    def __init__(
        self,
        url: str,
        echo: bool,
        max_overflow: int,
    ) -> None:
        self.engine = create_async_engine(
            url,
            echo=echo,
            max_overflow=max_overflow,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    async def dispose(self):
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session


db_helper = DBHelper(
    url=settings.db.url,
    echo=settings.db.echo,
    max_overflow=settings.db.max_overflow,
)
