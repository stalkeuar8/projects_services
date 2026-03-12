from app.models.hotel import Hotels
from app.schemas.hotels_schemas import HotelsSchema
from app.orms.base_orm import BaseOrm
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


class HotelsOrm(BaseOrm):

    @staticmethod
    async def create(incoming_data_dto: HotelsSchema, session: AsyncSession):
        hotel = Hotels(**incoming_data_dto.model_dump())

        session.add(hotel)


    @staticmethod
    async def multi_create(incoming_data_list_dto: list[HotelsSchema], session: AsyncSession):
        hotels = [
            Hotels(**hotel.model_dump()) for hotel in incoming_data_list_dto
        ]

        session.add_all(hotels)
    

    @staticmethod
    async def find_by_id(id_to_find: int, session: AsyncSession):
        query = (
            select(Hotels)
            .filter_by(id=id_to_find)
        )
        result = await session.execute(query)
        hotel = result.scalar_one_or_none()
        return hotel
    

    @staticmethod
    async def delete_by_id(id_to_delete: int, session: AsyncSession):
        query = (
            delete(Hotels)
            .where(Hotels.id == id_to_delete)
            .returning(Hotels)
        )
        result = await session.execute(query)
        hotel_to_delete = result.scalar_one_or_none()

        if not hotel_to_delete:
            raise ValueError("Room was not found")
            
        return hotel_to_delete



