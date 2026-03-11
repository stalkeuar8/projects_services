from app.schemas.bookings_schemas import BookingsSchema
from app.models.booking import Bookings, Clients
from app.utils.transaction_deco import transaction
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
import datetime

class BookingsOrm:

    @transaction
    @staticmethod
    async def new_booking(incoming_data_dto: BookingsSchema, session: AsyncSession | None = None):

        booking = Bookings(**incoming_data_dto.model_dump())
            
        session.add(booking)
        await session.flush()

        booking_id = booking.id

        await session.commit()
        return booking_id



    @transaction
    @staticmethod
    async def find_by_id(id_to_find: int, session: AsyncSession | None = None):
        query = (
            select(Bookings)
            .filter_by(id=id_to_find)
        )
        result = await session.execute(query)
        booking = result.scalar()
        return booking



    @transaction
    @staticmethod
    async def multi_find_by_ids(ids_to_find_list: list[int], session: AsyncSession | None = None):
        query = (
            select(Bookings)
            .where(Bookings.id.in_(ids_to_find_list))
            .order_by(Bookings.id)
        )
        results = await session.execute(query)
        bookings = results.scalars().all()
        return bookings


    @transaction
    @staticmethod
    async def find_by_client_id(client_id: int, session: AsyncSession | None = None):
        query = (
            select(Bookings)
            .filter_by(client_id=client_id)
        )
        result = await session.execute(query)
        booking = result.scalar()
        return booking


    @transaction
    @staticmethod 
    async def find_by_room_id(room_id: int, session: AsyncSession | None = None):
        query = (
            select(Bookings)
            .filter_by(room_id=room_id)
        )
        result = await session.execute(query)
        booking = result.scalar()
        return booking


    @transaction
    @staticmethod
    async def find_by_hotel_id(hotel_id: int, session: AsyncSession | None = None):
        query = (
            select(Bookings)
            .filter_by(hotel_id=hotel_id)
        )
        result = await session.execute(query)
        booking = result.scalar()
        return booking
    

    @transaction
    @staticmethod
    async def check_is_available(room_id: int, check_in: datetime.datetime, check_out: datetime.datetime, session: AsyncSession | None = None):
        query = (
            select(Bookings)
            .where(
                Bookings.room_id == room_id,
                Bookings.status != 'canceled', 
                Bookings.check_in < check_out, 
                Bookings.check_out > check_in
            )
            .order_by(Bookings.id.desc())
        )
        result = await session.execute(query)
        booking = result.scalars().first()
        if booking:
            return False
        
        return True