import asyncio
import datetime
import random
from typing import Sequence

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Bookings
from app.models.hotel import Rooms
from app.repo.bookings_repo import BookingsRepo
from app.repo.rooms_repo import RoomsRepo
from app.schemas.bookings_schemas import BookingsCreateSchema, BookingsPreparationSchema, BookingStatus
from app.schemas.rooms_schemas import RoomSearchFilters
from app.settings.database import async_session_factory


class BookingService:
    async def search_matching_rooms(self, filters: RoomSearchFilters, session: AsyncSession) -> Sequence[Rooms]:
        print(f"Finding matching rooms by filters: {filters.model_dump(exclude_none=True)}")

        rooms = await RoomsRepo.find_room_by_filters(filters=filters, session=session)

        return rooms

    async def _check_available(self, dto: BookingsPreparationSchema, session: AsyncSession) -> bool:
        room_id = dto.room_id
        check_in = dto.check_in
        check_out = dto.check_out

        room_status: bool = await BookingsRepo.check_is_available(room_id=room_id, check_in=check_in, check_out=check_out, session=session)

        return room_status

    async def _prepare_dto(self, short_dto: BookingsPreparationSchema, session: AsyncSession) -> BookingsCreateSchema:

        price_per_night = await RoomsRepo.get_price_per_night(id_to_find=short_dto.room_id, session=session)
        total_days = (short_dto.check_out - short_dto.check_in).days

        dto = BookingsCreateSchema(
            room_id=short_dto.room_id,
            client_id=short_dto.client_id,
            check_in=short_dto.check_in,
            check_out=short_dto.check_out,
            total_price=total_days * price_per_night,
            status=BookingStatus("pending"),
        )

        return dto

    async def new_booking(self, dto: BookingsPreparationSchema, session: AsyncSession) -> Bookings | None:
        obj_to_check = BookingsPreparationSchema(room_id=dto.room_id, check_in=dto.check_in, check_out=dto.check_out, client_id=dto.client_id)

        availability_result = await self._check_available(dto=obj_to_check, session=session)

        if availability_result:
            new_booking_info = await self._prepare_dto(short_dto=dto, session=session)
            new_booking = await BookingsRepo.create(inserting_data_dto=new_booking_info, session=session)

            return new_booking

        return None

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
