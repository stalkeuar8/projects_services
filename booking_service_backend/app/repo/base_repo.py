from typing import Any, Generic, Sequence, Type, TypeVar, cast

from pydantic import BaseModel
from sqlalchemy import ColumnElement, delete, inspect, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapper

from app.models.base import Base
from app.settings.database import async_engine, async_session_factory

# async def create_tables() -> None:
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


T = TypeVar("T")


class BaseRepo(Generic[T]):
    model: Type[T] | None = None

    @classmethod
    async def find_by_id(cls, session: AsyncSession, id_to_find: int) -> T | None:

        if cls.model:
            query = select(cls.model).where(cls.model.id == id_to_find, cls.model.deleted_at == None)

            result = await session.execute(query)
            found_obj = result.scalar()

            return found_obj

        raise ValueError()
