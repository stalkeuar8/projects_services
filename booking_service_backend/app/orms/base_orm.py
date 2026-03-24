from typing import Any, Generic, Sequence, Type, TypeVar, cast

from pydantic import BaseModel
from sqlalchemy import delete, inspect, select, ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapper

from app.models.base import Base
from app.settings.database import async_engine, async_session_factory


async def create_tables() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


T = TypeVar("T")


class BaseOrm(Generic[T]):
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
    async def find_all(cls, session: AsyncSession, filters: dict[str, Any]) -> Sequence[T] | None:

        if cls.model:
            mapper: Mapper[Any] = cast(Mapper[Any], inspect(cls.model))
            valid_columns = [column.key for column in mapper.attrs]

            for key in filters:
                if key not in valid_columns:
                    raise ValueError(f"{cls.model} ERROR: param '{key}' does not exists in '{cls.model}' model")

            query = select(cls.model).filter_by(**filters)

            results = await session.execute(query)
            found_objs = results.scalars().all()

            if not found_objs:
                return None

            return found_objs

        raise ValueError()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, filters: dict[str, Any]) -> T:

        if cls.model:
            mapper: Mapper[Any] = cast(Mapper[Any], inspect(cls.model))
            valid_columns = [column.key for column in mapper.attrs]

            for key in filters:
                if key not in valid_columns:
                    raise ValueError(f"{cls.model} ERROR: param '{key}' does not exists in '{cls.model}' model")

            query = select(cls.model).filter_by(**filters)

            result = await session.execute(query)
            found_obj = result.scalar_one_or_none()

            if not found_obj:
                raise ValueError("Object was not found")

            return found_obj

        raise ValueError()


    @classmethod
    async def fing_by_id(cls, session: AsyncSession, id_to_find: int) -> T | None:

        if cls.model:
            
            query = (
                select(cls.model)
                .filter_by(id=id_to_find)
            )

            result = await session.execute(query)
            found_obj = result.scalar()

            return found_obj

        raise ValueError()


    @classmethod
    async def delete_by_id(cls, session: AsyncSession, id_to_delete: int) -> T:

        if cls.model:
            query = delete(cls.model).filter_by(id=id_to_delete).returning(cls.model)
            result = await session.execute(query)
            deleted_obj = result.scalar_one_or_none()

            if not deleted_obj:
                raise ValueError(f"{cls.model} ERROR: obj with id '{id_to_delete}' does not exists in '{cls.model}' model")

            return deleted_obj

        raise ValueError()


    # @classmethod
    # async def find_one_or_none(cls, session: AsyncSession, *criteria: ColumnElement) -> T:

    #     if cls.model is not None:
    #         mapper: Mapper[Any] = cast(Mapper[Any], inspect(cls.model))
    #         valid_columns = [column.key for column in mapper.attrs]

    #         for key in filters:
    #             if key not in valid_columns:
    #                 raise ValueError(f"{cls.model} ERROR: param '{key}' does not exists in '{cls.model}' model")

    #         query = select(cls.model).filter_by(**filters)

    #         result = await session.execute(query)
    #         found_obj = result.scalar_one_or_none()

    #         if not found_obj:
    #             raise ValueError("Object was not found")

    #         return found_obj

    #     raise ValueError()
