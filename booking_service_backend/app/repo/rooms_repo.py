from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from app.models.hotel import Hotels, Rooms
from app.repo.base_repo import BaseRepo
from app.schemas.rooms_schemas import RoomSearchFilters


class RoomsRepo(BaseRepo[Rooms]):
    model = Rooms

    @staticmethod
    async def get_price_per_night(id_to_find: int, session: AsyncSession) -> int:
        query = select(Rooms).where(Rooms.id == id_to_find)
        result = (await session.execute(query)).scalar()

        if result:
            price: int = result.price_per_night
            return price

        raise ValueError("ERROR While getting price per night.")

    @staticmethod
    async def find_room_by_filters(filters: RoomSearchFilters, session: AsyncSession) -> Sequence[Rooms]:

        query = select(Rooms).join(Rooms.hotel)

        if filters.country:
            query = query.where(Hotels.country == filters.country)

        if filters.city:
            query = query.where(Hotels.city == filters.city)

        if filters.min_rating:
            query = query.where((Hotels.rating > filters.min_rating) | (Hotels.rating == filters.min_rating))

        if filters.max_rating:
            query = query.where((Hotels.rating < filters.max_rating) | (Hotels.rating == filters.max_rating))

        if filters.category:
            query = query.where(Rooms.category == filters.category)

        if filters.min_capacity:
            query = query.where((Rooms.capacity > filters.min_capacity) | (Rooms.capacity == filters.min_capacity))

        if filters.max_capacity:
            query = query.where((Rooms.capacity < filters.max_capacity) | (Rooms.capacity == filters.max_capacity))

        if filters.min_price:
            query = query.where((Rooms.price_per_night > filters.min_price) | (Rooms.price_per_night == filters.min_price))

        if filters.max_price:
            query = query.where((Rooms.price_per_night < filters.max_price) | (Rooms.price_per_night == filters.max_price))

        query = query.options(contains_eager(Rooms.hotel))

        results = await session.execute(query)
        rooms = results.scalars().all()

        return rooms
