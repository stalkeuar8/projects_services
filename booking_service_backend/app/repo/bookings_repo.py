import datetime
from typing import Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, selectinload

from app.models.booking import Bookings
from app.models.hotel import Rooms
from app.schemas.bookings_schemas import BookingsCreateSchema, BookingsStatsRequestSchema, BookingStatsResponseSchema, BookingStatus


class BookingsRepo:
    @staticmethod
    async def new_booking(inserting_data_dto: BookingsCreateSchema, session: AsyncSession) -> Bookings | None:
        new_obj = Bookings(**inserting_data_dto.model_dump())

        session.add(new_obj)
        await session.flush()

        return new_obj

    @staticmethod
    async def find_my_booking_by_id(session: AsyncSession, booking_id: int, current_user_id: int) -> Bookings | None:

        query = select(Bookings).where(Bookings.id == booking_id).where(Bookings.user_id == current_user_id)

        result = await session.execute(query)
        booking = result.scalar()

        return booking

    @staticmethod
    async def find_all_my_bookings(session: AsyncSession, current_user_id: int) -> Bookings | None:

        query = select(Bookings).where(Bookings.user_id == current_user_id)

        result = await session.execute(query)
        booking = result.scalar()

        return booking

    @staticmethod
    async def cancel_my_booking_by_id(booking_id: int, current_user_id: int, session: AsyncSession) -> Bookings | None:

        query = (
            update(Bookings)
            .where(Bookings.id == booking_id, Bookings.user_id == current_user_id)
            .values(status=BookingStatus("canceled"))
            .returning(Bookings)
        )

        result = await session.execute(query)
        canceled_booking = result.scalar()

        return canceled_booking

    @staticmethod
    async def check_is_available(
        room_id: int,
        check_in: datetime.datetime,
        check_out: datetime.datetime,
        session: AsyncSession,
    ) -> bool:
        query = (
            select(Bookings)
            .where(Bookings.status != "canceled", Bookings.check_in < check_out, Bookings.check_out > check_in, Bookings.room_id == room_id)
            .order_by(Bookings.id.desc())
            .with_for_update(nowait=True)
        )
        result = await session.execute(query)
        booking = result.scalars().first()
        if booking:
            return False

        return True

    @staticmethod
    async def get_not_available_rooms(check_in: datetime.datetime, check_out: datetime.datetime, session: AsyncSession) -> list[int | None]:
        query = (
            select(Bookings.room_id)
            .where(
                Bookings.status != "canceled",
                Bookings.check_in > check_out,
                Bookings.check_out < check_in,
            )
            .order_by(Bookings.id.desc())
        )

        results = await session.execute(query)

        ids = results.scalars().all()

        return ids


class AdminBookingsRepo:
    @staticmethod
    async def admin_find_by_id(session: AsyncSession, booking_id: int) -> Bookings | None:

        query = select(Bookings).where(Bookings.id == booking_id)

        result = await session.execute(query)
        booking = result.scalar()

        return booking

    @staticmethod
    async def admin_find_by_hotel_id(hotel_id: int, session: AsyncSession, limit: int = 10) -> Sequence[Bookings] | None:
        query = (
            select(Bookings)
            .join(Bookings.room)
            .where(Bookings.status != "canceled")
            .where(Rooms.hotel_id == hotel_id)
            .options(contains_eager(Bookings.room))
            .order_by(Bookings.created_at.desc())
            .limit(limit)
        )

        results = await session.execute(query)
        bookings = results.scalars().all()

        if bookings:
            return bookings

        return None

    @staticmethod
    async def admin_change_booking_status(booking_id: int, new_status: BookingStatus, session: AsyncSession) -> Bookings | None:
        query = update(Bookings).where(Bookings.id == booking_id).values(status=new_status).returning(Bookings)

        result = await session.execute(query)
        updated_booking = result.scalar()

        return updated_booking

    @staticmethod
    async def admin_delete_booking(booking_id: int, session: AsyncSession) -> Bookings | None:

        query = delete(Bookings).where(Bookings.id == booking_id).returning(Bookings)

        result = await session.execute(query)
        deleted_booking = result.scalar()

        return deleted_booking

    @staticmethod
    async def admin_get_bookings_stats(filters: BookingsStatsRequestSchema, session: AsyncSession) -> BookingStatsResponseSchema | None:

        query = select(Bookings)

        if filters.created_after:
            query = query.where(Bookings.created_at >= filters.created_after)

        if filters.created_before:
            query = query.where(Bookings.created_at <= filters.created_before)

        if filters.room_id:
            query = query.where(Bookings.room_id == filters.room_id)

        if filters.hotel_id:
            query = query.join(Rooms).where(Rooms.hotel_id == filters.hotel_id).options(contains_eager(Bookings.room))

        result = await session.execute(query)
        bookings = result.scalars().all()

        if bookings:
            response_obj = BookingStatsResponseSchema(
                total_bookings=len(bookings),
                total_booked_bookings=len([booking for booking in bookings if booking.status == "booked"]),
                total_canceled_bookings=len([booking for booking in bookings if booking.status == "canceled"]),
                total_completed_bookings=len([booking for booking in bookings if booking.status == "completed"]),
                total_checked_in_bookings=len([booking for booking in bookings if booking.status == "checked_in"]),
                total_pending_bookings=len([booking for booking in bookings if booking.status == "pending"]),
            )

            return response_obj

        return None
