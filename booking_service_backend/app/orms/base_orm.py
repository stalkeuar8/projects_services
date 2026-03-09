from app.models.base import Base
from app.models.booking import Bookings, Clients
from app.models.hotel import Hotels, Rooms
from app.utils.booking_validators import BookingsSchema
from app.utils.hotel_validators import HotelsSchema, RoomsSchema
from app.settings.database import async_session_factory, async_engine
from app.utils.transaction_deco import transaction
from abc import ABC, abstractmethod
import asyncio

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class BaseOrm(ABC):

    @staticmethod
    @abstractmethod
    async def create(inserting_data: dict):
        pass

    @staticmethod
    @abstractmethod
    async def multi_create(inserting_data_list: list[dict]):
        pass


    @staticmethod
    @abstractmethod
    async def find_by_id(id_to_find: int):
        pass


    @staticmethod
    @abstractmethod
    async def delete_by_id(id_to_delete: int):
        pass


    
    
