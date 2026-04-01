from datetime import datetime, timezone
from typing import Any, Generic, Sequence, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import cast, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base
from app.settings.database import async_session_factory

T = TypeVar("T", bound=Base)


class BaseAdminRepo(Generic[T]):
    model: Type[T]

    @classmethod
    async def create(cls, session: AsyncSession, inserting_data_dto: BaseModel) -> T:

        new_obj = cls.model(**inserting_data_dto.model_dump())

        session.add(new_obj)
        await session.flush()

        return new_obj

    @classmethod
    async def multi_create(cls, session: AsyncSession, inserting_data_list_dto: Sequence[BaseModel]) -> Sequence[T]:

        new_objs = [cls.model(**obj_info.model_dump()) for obj_info in inserting_data_list_dto]

        session.add_all(new_objs)
        await session.flush()

        return new_objs

    @classmethod
    async def admin_find_by_id(cls, session: AsyncSession, id_to_find: int) -> T | None:

        query = select(cls.model).where(cast(Any, cls.model.id) == id_to_find, cast(Any, cls.model.deleted_at).is_(None))

        result = await session.execute(query)
        found_obj = result.scalar_one_or_none()

        return found_obj

    @classmethod
    async def admin_delete_by_id(cls, session: AsyncSession, id_to_delete: int) -> T | None:

        current_time = datetime.now(tz=timezone.utc)

        query = update(cls.model).where(cast(Any, cls.model.id) == id_to_delete).values(deleted_at=current_time).returning(cls.model)

        result = await session.execute(query)
        deleted_obj = result.scalar_one_or_none()

        return deleted_obj
