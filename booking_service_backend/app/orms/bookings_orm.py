from app.utils.booking_validators import BookingsSchema
from app.models.booking import Bookings, Clients
from app.orms.base_orm import BaseOrm
from app.settings.database import async_session_factory
from sqlalchemy import select
import asyncio


class BookingsOrm(BaseOrm):

    @staticmethod
    async def new_client(incoming_data: dict):
        async with async_session_factory() as session:
            new_client = Clients(**incoming_data)
            session.add(new_client)
            await session.commit()


    @staticmethod
    async def new_clients(incoming_data_list: list[dict]):
        async with async_session_factory() as session:
            clients = [
                Clients(**client) for client in incoming_data_list
            ]

            session.add_all(clients)
            await session.commit()


    @staticmethod
    async def new_booking(incoming_data: dict):
        async with async_session_factory() as session:
            validated_data = BookingsSchema.model_validate(incoming_data)

            booking = Bookings(**validated_data.model_dump())
            
            session.add(booking)
            await session.commit()



    