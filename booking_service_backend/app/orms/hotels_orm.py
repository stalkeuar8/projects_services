from app.models.hotel import Hotels
from app.schemas.hotels_schemas import HotelsSchema
from app.orms.base_orm import BaseOrm
from app.utils.transaction_deco import transaction
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


class HotelsOrm(BaseOrm):

    @transaction
    @staticmethod
    async def create(incoming_data_dto: HotelsSchema, session: AsyncSession | None = None):
        hotel = Hotels(**incoming_data_dto.model_dump())

        session.add(hotel)


    @transaction
    @staticmethod
    async def multi_create(incoming_data_list_dto: list[HotelsSchema], session: AsyncSession | None = None):
        hotels = [
            Hotels(**hotel.model_dump()) for hotel in incoming_data_list_dto
        ]

        session.add_all(hotels)
    

    @transaction
    @staticmethod
    async def find_by_id(id_to_find: int, session: AsyncSession | None = None):
        query = (
            select(Hotels)
            .filter_by(id=id_to_find)
        )
        result = await session.execute(query)
        hotel = result.scalar_one_or_none()
        return hotel
    

    @transaction
    @staticmethod
    async def delete_by_id(id_to_delete: int, session: AsyncSession | None = None):
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



