from app.models.base import Base
from app.models.booking import Bookings, Clients
from app.models.hotel import Hotels, Rooms
from app.utils.booking_validators import BookingsSchema
from app.utils.hotel_validators import HotelsSchema, RoomsSchema
from app.settings.database import async_session_factory, async_engine
from abc import ABC
import asyncio

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class BaseOrm(ABC):
    pass
