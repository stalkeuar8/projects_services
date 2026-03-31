from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.settings.config import database_settings

async_engine: AsyncEngine = create_async_engine(url=database_settings.DATABASE_async_url, echo=False, pool_size=5, max_overflow=10)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)

celery_engine: AsyncEngine = create_async_engine(url=database_settings.DATABASE_async_url, echo=False, pool_size=5, max_overflow=10)
celery_session_factory = async_sessionmaker(celery_engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory.begin() as session:
        yield session
