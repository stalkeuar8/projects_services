from app.models.booking import Bookings
from app.models.hotel import Rooms
from app.orms.base_orm import BaseOrm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager
import datetime


class BookingsOrm(BaseOrm[Bookings]):

    model = Bookings


    @staticmethod
    async def find_by_hotel_id(hotel_id: int, session: AsyncSession):
        query = select(Bookings).join(Bookings.room).where(Rooms.hotel_id==hotel_id).options(contains_eager(Bookings.room))
        result = await session.execute(query)
        booking = result.scalar()
        return booking


    @staticmethod
    async def check_is_available(
        room_id: int,
        check_in: datetime.datetime,
        check_out: datetime.datetime,
        session: AsyncSession,
    ):
        query = (
            select(Bookings)
            .where(
                Bookings.room_id == room_id,
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
