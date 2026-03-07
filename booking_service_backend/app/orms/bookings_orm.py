from app.utils.booking_validators import BookingsSchema
from app.models.booking import Bookings, Clients
from app.settings.database import async_session_factory, async_engine
from sqlalchemy import select
import asyncio
from faker import Faker
import random

fake = Faker('en_US')

BANNED_COUNTRIES = [
    'Russia', 'Russian Federation', 
    'Belarus', 'Republic of Belarus'
]


class BookingsOrm:

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
    async def new_booking():
        pass
