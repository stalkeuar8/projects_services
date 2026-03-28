import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager, selectinload

from app.models.booking import Bookings
from app.models.hotel import Rooms
from app.repo.base_repo import BaseRepo


class BookingsRepo(BaseRepo[Bookings]):
    model = Bookings

    @staticmethod
    async def find_by_id(session: AsyncSession, booking_id: int, current_user_id: int | None = None) -> Bookings | None:
        
        query = (
            select(Bookings)
            .where(Bookings.id==booking_id)
        )

        if current_user_id:
            query = query.where(Bookings.user_id==current_user_id)

        result = await session.execute(query)
        booking = result.scalar()

        return booking

    @staticmethod
    async def find_by_hotel_id(hotel_id: int, session: AsyncSession) -> Bookings | None:
        query = select(Bookings).join(Bookings.room).where(Rooms.hotel_id == hotel_id).options(contains_eager(Bookings.room))
        result = await session.execute(query)
        booking = result.scalar_one_or_none()
        return booking


    @staticmethod
    async def change_booking_status(booking_id: int, new_status: str, session: AsyncSession) -> Bookings | None:
        query = (
            update(Bookings)
            .where(Bookings.id==booking_id)
            .values(status=new_status)
            .returning(True)
        )

        result = await session.execute(query)
        updated_booking = result.scalar()

        return updated_booking 



    @staticmethod
    async def check_is_available(
        room_id: int,
        check_in: datetime.datetime,
        check_out: datetime.datetime,
        session: AsyncSession,
    ) -> bool:
        query = (
            select(Bookings)
            .where(
                Bookings.status != "canceled",
                Bookings.check_in < check_out,
                Bookings.check_out > check_in,
            )
            .order_by(Bookings.id.desc())
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
        # subq = (
        #     select(Bookings.room_id.distinct())
        # )

        # subq_results = await session.execute(subq)
        # ids = subq_results.scalars().all()

        # rooms_query = (
        #     select(Rooms)
        #     .where(Rooms.id.not_in(ids))
        # )

        # bookings_query_results = await session.execute(bookings_query)
        # rooms_ids_bookings = bookings_query_results.scalars().all()

        # rooms_query_results = await session.execute(rooms_query)
        # rooms_ids = rooms_query_results.scalars().all()

        # available_rooms = []

        # if rooms_ids_bookings:
        #     for room_id in rooms_ids_bookings:
        #         available_rooms.append(room_id)

        # if rooms_ids:
        #     for room_id in rooms_ids:
        #         available_rooms.append(room_id)

        # return available_rooms
