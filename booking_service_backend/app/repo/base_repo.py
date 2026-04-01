from typing import Any, Generic, Type, TypeVar

from sqlalchemy import cast, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base
from app.settings.database import async_session_factory

T = TypeVar("T", bound=Base)


class BaseRepo(Generic[T]):
    model: Type[T]

    @classmethod
    async def find_by_id(cls, session: AsyncSession, id_to_find: int) -> T | None:

        query = select(cls.model).where(cast(Any, cls.model.id) == id_to_find, cast(Any, cls.model.deleted_at).is_(None))

        result = await session.execute(query)
        found_obj = result.scalar_one_or_none()

        return found_obj
