from app.schemas.bookings_schemas import BookingsSchema
from app.models.booking import Bookings, Clients
from app.utils.transaction_deco import transaction
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio


class BookingsOrm:

    @transaction
    @staticmethod
    async def new_booking(incoming_data: dict, session: AsyncSession | None = None):
        validated_data = BookingsSchema.model_validate(incoming_data)

        booking = Bookings(**validated_data.model_dump())
            
        session.add(booking)
        await session.commit()



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
    async def check_room_status(room_id: int, session: AsyncSession | None = None):
        query = (
            select(Bookings)
            .filter_by(room_id=room_id)
            .order_by(Bookings.id.desc())
            .limit(1)
        )
        result = await session.execute(query)
        room_info = result.scalar_one_or_none()

        return room_info
