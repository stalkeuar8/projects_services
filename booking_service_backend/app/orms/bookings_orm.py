from app.utils.booking_validators import BookingsSchema
from app.models.booking import Bookings, Clients
from app.orms.base_orm import BaseOrm
from app.settings.database import async_session_factory
from sqlalchemy import select
import asyncio


class BookingsOrm:


    @staticmethod
    async def new_booking(incoming_data: dict):
        async with async_session_factory() as session:
            validated_data = BookingsSchema.model_validate(incoming_data)

            booking = Bookings(**validated_data.model_dump())
            
            session.add(booking)
            await session.commit()



    @staticmethod
    async def find_by_id(id_to_find: int):
        async with async_session_factory() as session:
            query = (
                select(Bookings)
                .filter_by(id=id_to_find)
            )
            booking = await session.execute(query).scalar()
            return booking



    @staticmethod
    async def multi_find_by_ids(ids_to_find_list: list[int]):
        async with async_session_factory() as session:
            query = (
                select(Bookings)
                .where(Bookings.id.in_(ids_to_find_list))
                .order_by(Bookings.id)
            )
            bookings = await session.execute(query).scalars().all()
            return bookings


    @staticmethod
    async def find_by_client_id(client_id: int):
        async with async_session_factory() as session:
            query = (
                select(Bookings)
                .filter_by(client_id=client_id)
            )
            booking = await session.execute(query).scalar()
            return booking


    @staticmethod 
    async def find_by_room_id(room_id: int):
        async with async_session_factory() as session:
            query = (
                select(Bookings)
                .filter_by(room_id=room_id)
            )
            booking = await session.execute(query).scalar()
            return booking


    @staticmethod
    async def find_by_hotel_id(hotel_id: int):
        async with async_session_factory() as session:
            query = (
                select(Bookings)
                .filter_by(hotel_id=hotel_id)
            )
            booking = await session.execute(query).scalar()
            return booking