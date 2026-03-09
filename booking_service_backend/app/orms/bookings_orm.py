from app.utils.booking_validators import BookingsSchema
from app.models.booking import Bookings, Clients
from app.orms.base_orm import BaseOrm
from app.settings.database import async_session_factory
from app.utils.transaction_deco import transaction
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio


class BookingsOrm:

    @transaction
    @staticmethod
    async def new_booking(session: AsyncSession, incoming_data: dict):
        validated_data = BookingsSchema.model_validate(incoming_data)

        booking = Bookings(**validated_data.model_dump())
            
        session.add(booking)
        await session.commit()



    @transaction
    @staticmethod
    async def find_by_id(session: AsyncSession, id_to_find: int):
        query = (
            select(Bookings)
            .filter_by(id=id_to_find)
        )
        booking = await session.execute(query).scalar()
        return booking



    @transaction
    @staticmethod
    async def multi_find_by_ids(session: AsyncSession, ids_to_find_list: list[int]):
        query = (
            select(Bookings)
            .where(Bookings.id.in_(ids_to_find_list))
            .order_by(Bookings.id)
        )
        bookings = await session.execute(query).scalars().all()
        return bookings


    @transaction
    @staticmethod
    async def find_by_client_id(session: AsyncSession, client_id: int):
        query = (
            select(Bookings)
            .filter_by(client_id=client_id)
        )
        booking = await session.execute(query).scalar()
        return booking


    @transaction
    @staticmethod 
    async def find_by_room_id(session: AsyncSession, room_id: int):
        query = (
            select(Bookings)
            .filter_by(room_id=room_id)
        )
        booking = await session.execute(query).scalar()
        return booking


    @transaction
    @staticmethod
    async def find_by_hotel_id(session: AsyncSession, hotel_id: int):
        query = (
            select(Bookings)
            .filter_by(hotel_id=hotel_id)
        )
        booking = await session.execute(query).scalar()
        return booking