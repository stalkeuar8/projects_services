from app.models.hotel import Rooms
from app.utils.hotel_validators import RoomsSchema, rooms_adapter
from app.orms.base_orm import BaseOrm
from app.utils.transaction_deco import transaction
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


class RoomsOrm(BaseOrm):


    @transaction
    @staticmethod
    async def create(session: AsyncSession, incoming_data: dict):
        validated_data = RoomsSchema.model_validate(incoming_data)
        room = Rooms(**validated_data.model_dump())

        session.add(room)



    @transaction
    @staticmethod
    async def multi_create(session: AsyncSession, incoming_data_list: list[dict]):
        validated_data_list = rooms_adapter.validate_python(incoming_data_list)

        rooms = [
            Rooms(**room.model_dump()) for room in validated_data_list
        ]

        session.add_all(rooms)


    @transaction
    @staticmethod
    async def find_by_id(session: AsyncSession, id_to_find: int):
        query = (
            select(Rooms)
            .filter_by(id=id_to_find)
        )
        room = await session.execute(query).scalar_one_or_none()
        return room
    

    @transaction
    @staticmethod
    async def delete_by_id(session: AsyncSession, id_to_delete: int):
        query = (
            delete(Rooms)
            .where(Rooms.id == id_to_delete)\
            .returning(Rooms)
        )
        room = await session.execute(query)
        room_to_delete = room.scalar_one_or_none()

        if not room_to_delete:
            raise ValueError("Room was not found")
            
        return room_to_delete


    