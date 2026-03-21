from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from app.settings.config import database_settings

async_engine: AsyncEngine = create_async_engine(
    url=database_settings.DATABASE_async_url, echo=False, pool_size=5, max_overflow=10
)

async_session_factory = async_sessionmaker(async_engine, expire_on_commit=False)
