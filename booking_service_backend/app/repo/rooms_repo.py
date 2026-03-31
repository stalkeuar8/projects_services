from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from app.models.booking import Bookings
from app.models.hotel import Hotels, Rooms
from app.repo.base_admin_repo import BaseAdminRepo
from app.repo.base_repo import BaseRepo
from app.schemas.rooms_schemas import RoomEditSchema, RoomSearchFilters


class RoomsRepo(BaseRepo[Rooms]):
    model = Rooms

    @staticmethod
    async def get_price_per_night(id_to_find: int, session: AsyncSession) -> int:
        query = select(Rooms).where(Rooms.id == id_to_find).where(Rooms.deleted_at is None)
        result = (await session.execute(query)).scalar()

        if result:
            price: int = result.price_per_night
            return price

        raise ValueError("ERROR While getting price per night.")

    @staticmethod
    async def find_room_by_filters(filters: RoomSearchFilters, session: AsyncSession) -> Sequence[Rooms]:

        query = select(Rooms).join(Rooms.hotel).where(Rooms.deleted_at is None)

        if filters.check_in and filters.check_out:
            subquery = select(Bookings.room_id).where(
                Bookings.status != "canceled",
                Bookings.check_in < filters.check_out,
                Bookings.check_out > filters.check_in,
            )

            query = query.where(Rooms.id.not_in(subquery))

        if filters.country:
            query = query.where(Hotels.country == filters.country)

        if filters.city:
            query = query.where(Hotels.city == filters.city)

        if filters.min_rating:
            query = query.where(Hotels.rating >= filters.min_rating)

        if filters.max_rating:
            query = query.where(Hotels.rating <= filters.max_rating)

        if filters.category:
            query = query.where(Rooms.category == filters.category)

        if filters.min_capacity:
            query = query.where(Rooms.capacity >= filters.min_capacity)

        if filters.max_capacity:
            query = query.where(Rooms.capacity <= filters.max_capacity)

        if filters.min_price:
            query = query.where(Rooms.price_per_night >= filters.min_price)

        if filters.max_price:
            query = query.where(Rooms.price_per_night <= filters.max_price)

        query = query.options(contains_eager(Rooms.hotel))

        results = await session.execute(query)
        rooms = results.scalars().all()

        return rooms


class AdminRoomsRepo(BaseAdminRepo[Rooms]):
    model = Rooms

    @staticmethod
    async def admin_edit_room_info(room_id: int, session: AsyncSession, info_to_edit: RoomEditSchema) -> Rooms | None:
        query = update(Rooms).where(Rooms.id == room_id).where(Rooms.deleted_at is None)

        if info_to_edit.category:
            query = query.values(category=info_to_edit.category)

        if info_to_edit.capacity:
            query = query.values(capacity=info_to_edit.capacity)

        if info_to_edit.price_per_night:
            query = query.values(price_per_night=info_to_edit.price_per_night)

        if info_to_edit.hotel_id:
            query = query.values(hotel_id=info_to_edit.hotel_id)

        result = await session.execute(query)
        edited_room = result.scalar()

        return edited_room
