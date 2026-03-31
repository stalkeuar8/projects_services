from typing import Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.settings.database import async_session_factory


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
