import asyncio
import datetime
import random
from typing import Sequence

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Bookings
from app.models.hotel import Rooms
from app.orms.bookings_orm import BookingsOrm
from app.orms.rooms_orm import RoomsOrm
from app.schemas.bookings_schemas import BookingsCheckAvailableSchema, BookingsSchema, BookingStatus
from app.settings.database import async_session_factory
from app.utils.room_search_filter import RoomSearchFilters


class BookingService:
    async def search_matching_rooms(self, filters: RoomSearchFilters, session: AsyncSession) -> Sequence[Rooms]:
        print(f"Finding matching rooms by filters: {filters.model_dump(exclude_none=True)}")

        rooms = await RoomsOrm.find_room_by_filters(filters=filters, session=session)

        return rooms

    async def check_available(self, dto: BookingsCheckAvailableSchema, session: AsyncSession) -> bool:
        room_id = dto.room_id
        check_in = dto.check_in
        check_out = dto.check_out

        room_status: bool = await BookingsOrm.check_is_available(room_id=room_id, check_in=check_in, check_out=check_out, session=session)

        return room_status

    async def prepare_dto(self, short_dto: BookingsCheckAvailableSchema, session: AsyncSession) -> BookingsSchema:

        price_per_night = await RoomsOrm.get_price_per_night(id_to_find=short_dto.room_id, session=session)
        total_days = (short_dto.check_out - short_dto.check_in).days

        dto = BookingsSchema(
            room_id=short_dto.room_id,
            client_id=short_dto.client_id,
            check_in=short_dto.check_in,
            check_out=short_dto.check_out,
            total_price=total_days * price_per_night,
            status=BookingStatus("pending"),
        )

        return dto

    async def new_booking(self, dto: BookingsSchema, session: AsyncSession) -> Bookings:
        new_booking = await BookingsOrm.create(inserting_data_dto=dto, session=session)

        return new_booking

    async def approve_booking(self, booking_id: int) -> bool:
        print("\nApproving....\n")

        time_to_sleep = random.randint(5, 10)
        await asyncio.sleep(time_to_sleep)

        chance = random.randint(1, 100)

        is_successful = None

        if 90 <= chance <= 100:
            query = update(Bookings).values(status="canceled").where(Bookings.id == booking_id)
            is_successful = False

        else:
            query = update(Bookings).values(status="booked").where(Bookings.id == booking_id)
            is_successful = True

        async with async_session_factory() as session:
            await session.execute(query)
            await session.commit()

        return is_successful
