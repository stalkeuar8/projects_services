from app.models.hotel import Hotels
from app.utils.hotel_validators import HotelsSchema, hotels_adapter
from app.orms.base_orm import BaseOrm
from app.utils.transaction_deco import transaction
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


class HotelsOrm(BaseOrm):

    @transaction
    @staticmethod
    async def create(session: AsyncSession, incoming_data: dict):
        validated_data = HotelsSchema.model_validate(incoming_data)
        hotel = Hotels(**validated_data.model_dump())

        session.add(hotel)


    @transaction
    @staticmethod
    async def multi_create(session: AsyncSession, incoming_data_list: list[dict]):
        validated_data_list = hotels_adapter.validate_python(incoming_data_list)

        hotels = [
            Hotels(**hotel.model_dump()) for hotel in validated_data_list
        ]

        session.add_all(hotels)
    

    @transaction
    @staticmethod
    async def find_by_id(session: AsyncSession, id_to_find: int):
        query = (
            select(Hotels)
            .filter_by(id=id_to_find)
        )
        hotel = await session.execute(query).scalar_one_or_none()
        return hotel
    

    @transaction
    @staticmethod
    async def delete_by_id(session: AsyncSession, id_to_delete: int):
        query = (
            delete(Hotels)
            .where(Hotels.id == id_to_delete)\
            .returning(Hotels)
        )
        hotel = await session.execute(query)
        hotel_to_delete = hotel.scalar_one_or_none()

        if not hotel_to_delete:
            raise ValueError("Room was not found")
            
        return hotel_to_delete


    