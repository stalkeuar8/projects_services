from app.models.base import Base
from app.settings.database import async_session_factory, async_engine
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class BaseOrm(ABC):

    @staticmethod
    @abstractmethod
    async def create(session: AsyncSession, inserting_data: dict):
        pass

    @staticmethod
    @abstractmethod
    async def multi_create(session: AsyncSession, inserting_data_list: list[dict]):
        pass

    @staticmethod
    @abstractmethod
    async def find_by_id(session: AsyncSession, id_to_find: int):
        pass

    @staticmethod
    @abstractmethod
    async def delete_by_id(session: AsyncSession, id_to_delete: int):
        pass
