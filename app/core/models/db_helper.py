from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)

from app.core.config import settings


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        pool_timeout: int = 20,
        pool_recycle: int = 1200,
        pool_pre_ping: bool = True,
        max_overflow: int = 10,
    ):
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            pool_timeout=pool_timeout,
            pool_recycle=pool_recycle,
            pool_pre_ping=pool_pre_ping,
            max_overflow=max_overflow,
            connect_args={"prepared_statement_cache_size": 0},
            )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(  # noqa:E501
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_getter(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            async with session.begin():
                yield session


db_helper = DatabaseHelper(
    url=str(settings.db.url),
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    pool_size=settings.db.pool_size,
    pool_timeout=settings.db.pool_timeout,
    pool_recycle=settings.db.pool_recycle,
    pool_pre_ping=settings.db.pool_pre_ping,
    max_overflow=settings.db.max_overflow,
)
