from typing import Any, Generic, Sequence, Type, TypeVar, cast

from datetime import datetime, timezone

from pydantic import BaseModel
from sqlalchemy import ColumnElement, delete, inspect, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapper

from app.models.base import Base
from app.settings.database import async_engine, async_session_factory

T = TypeVar("T")


class BaseAdminRepo(Generic[T]):
    model: Type[T] | None = None

    @classmethod
    async def create(cls, session: AsyncSession, inserting_data_dto: BaseModel) -> T:

        if cls.model:
            new_obj = cls.model(**inserting_data_dto.model_dump())

            session.add(new_obj)
            await session.flush()

            return new_obj

        raise ValueError()


    @classmethod
    async def multi_create(cls, session: AsyncSession, inserting_data_list_dto: list[BaseModel]) -> Sequence[T]:

        if cls.model:
            new_objs = [cls.model(**obj_info.model_dump()) for obj_info in inserting_data_list_dto]

            session.add_all(new_objs)
            await session.flush()

            return new_objs

        raise ValueError()


    @classmethod
    async def admin_find_by_id(cls, session: AsyncSession, id_to_find: int) -> T | None:

        if cls.model:
            query = select(cls.model).where(cls.model.id == id_to_find, cls.model.deleted_at == None)

            result = await session.execute(query)
            found_obj = result.scalar()

            return found_obj

        raise ValueError()


    @classmethod
    async def admin_delete_by_id(cls, session: AsyncSession, id_to_delete: int) -> T | None:

        current_time = datetime.now(tz=timezone.utc)

        if cls.model:
            query = (
                update(cls.model)
                .where(cls.model.id==id_to_delete)
                .values(deleted_at=current_time)
                .returning(cls.model)
            )
            
            result = await session.execute(query)
            deleted_obj = result.scalar_one_or_none()

            return deleted_obj

        raise ValueError()