from app.models.hotel import Hotels, Rooms
from app.utils.hotel_validators import HotelsSchema, RoomsSchema, rooms_adapter, hotels_adapter
from app.settings.database import async_session_factory, async_engine
from app.orms.base_orm import BaseOrm
from sqlalchemy import select
import asyncio


class HotelsOrm(BaseOrm):

    @staticmethod
    async def new_hotel(incoming_data: dict):
        async with async_session_factory() as session:
            validated_data = HotelsSchema.model_validate(incoming_data)
            hotel = Hotels(**validated_data.model_dump())

            session.add(hotel)
            await session.commit()

    
    @staticmethod
    async def new_room(incoming_data: dict):
        async with async_session_factory() as session:
            validated_data = RoomsSchema.model_validate(incoming_data)
            room = Rooms(**validated_data.model_dump())

            session.add(room)
            await session.commit()


    @staticmethod
    async def new_hotels(incoming_data_list: list[dict]):
        async with async_session_factory() as session:
            validated_data_list = hotels_adapter.validate_python(incoming_data_list)

            hotels = [
                Hotels(**hotel.model_dump()) for hotel in validated_data_list
            ]

            session.add_all(hotels)
            await session.commit()
    

    @staticmethod
    async def new_rooms(incoming_data_list: list[dict]):
        async with async_session_factory() as session:
            validated_data_list = rooms_adapter.validate_python(incoming_data_list)

            rooms = [
                Rooms(**room.model_dump()) for room in validated_data_list
            ]

            session.add_all(rooms)
            await session.commit()



    