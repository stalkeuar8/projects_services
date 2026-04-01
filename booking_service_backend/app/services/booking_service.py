import asyncio
import random
from typing import Sequence

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Bookings
from app.models.hotel import Rooms
from app.repo.bookings_repo import BookingsRepo
from app.repo.rooms_repo import RoomsRepo
from app.schemas.bookings_schemas import AvailabilityForBookingRequestSchema, BookingsCreateSchema, BookingsPreparationSchema, BookingStatus
from app.schemas.rooms_schemas import RoomSearchFilters
from app.settings.database import async_session_factory


class BookingService:
    async def search_matching_rooms(self, filters: RoomSearchFilters, session: AsyncSession) -> Sequence[Rooms]:
        print(f"Finding matching rooms by filters: {filters.model_dump(exclude_none=True)}")

        if (filters.check_out and not filters.check_in) or (filters.check_in and not filters.check_out):
            raise ValueError

        rooms = await RoomsRepo.find_room_by_filters(filters=filters, session=session)

        return rooms

    async def check_available(self, dto: AvailabilityForBookingRequestSchema, session: AsyncSession) -> bool:
        room_id = dto.room_id
        check_in = dto.check_in
        check_out = dto.check_out

        room_status: bool = await BookingsRepo.check_is_available(room_id=room_id, check_in=check_in, check_out=check_out, session=session)

        return room_status

    async def _prepare_dto(self, user_id: int, short_dto: BookingsPreparationSchema, session: AsyncSession) -> BookingsCreateSchema:

        price_per_night = await RoomsRepo.get_price_per_night(id_to_find=short_dto.room_id, session=session)
        total_days = (short_dto.check_out - short_dto.check_in).days

        dto = BookingsCreateSchema(
            room_id=short_dto.room_id,
            user_id=user_id,
            check_in=short_dto.check_in,
            check_out=short_dto.check_out,
            total_price=total_days * price_per_night,
            status=BookingStatus("pending"),
        )

        return dto

    async def new_booking(self, user_id: int, dto: BookingsPreparationSchema, session: AsyncSession) -> Bookings | None:
        obj_to_check = AvailabilityForBookingRequestSchema(room_id=dto.room_id, check_in=dto.check_in, check_out=dto.check_out)

        availability_result = await self.check_available(dto=obj_to_check, session=session)

        if availability_result:
            new_booking_info = await self._prepare_dto(short_dto=dto, user_id=user_id, session=session)
            new_booking = await BookingsRepo.new_booking(inserting_data_dto=new_booking_info, session=session)

            return new_booking

        return None
