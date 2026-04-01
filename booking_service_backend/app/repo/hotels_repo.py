from typing import Sequence

import bcrypt
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hotel import HotelAdmins, Hotels
from app.repo.base_admin_repo import BaseAdminRepo
from app.repo.base_repo import BaseRepo
from app.schemas.auth.hotel_bot_schemas import HotelLoginSchema
from app.schemas.hotels_schemas import HotelEditSchema, HotelsCreateSchema, HotelSearchFilters, HotelsCreateListSchema


class HotelsRepo(BaseRepo[Hotels]):
    model = Hotels

    @staticmethod
    async def find_hotel_by_filters(filters: HotelSearchFilters, session: AsyncSession) -> Sequence[Hotels] | None:

        query = select(Hotels).where(Hotels.deleted_at.is_(None))

        if filters.country:
            query = query.where(Hotels.country == filters.country)

        if filters.city:
            query = query.where(Hotels.city == filters.city)

        if filters.min_rating:
            query = query.where((Hotels.rating > filters.min_rating) | (Hotels.rating == filters.min_rating))

        if filters.max_rating:
            query = query.where((Hotels.rating < filters.max_rating) | (Hotels.rating == filters.max_rating))

        results = await session.execute(query)
        rooms = results.scalars().all()

        return rooms


class AdminHotelsRepo(BaseAdminRepo[Hotels]):
    model = Hotels

    @classmethod
    async def create(cls, session: AsyncSession, inserting_data_dto: BaseModel) -> Hotels:

        new_obj = Hotels(**inserting_data_dto.model_dump())

        session.add(new_obj)
        await session.flush()

        hashed_password = bcrypt.hashpw(f"password_hotel{new_obj.id}".encode("utf-8"), bcrypt.gensalt())

        new_hotel_admin_obj = HotelAdmins(hotel_id=new_obj.id, bot_hashed_password=hashed_password)
        session.add(new_hotel_admin_obj)

        return new_obj

    @staticmethod
    async def multi_create(session: AsyncSession, inserting_data_list_dto: HotelsCreateListSchema) -> Sequence[Hotels]:
        hotels: Sequence[HotelsCreateSchema] = inserting_data_list_dto.hotels_list

        new_hotel_objs: Sequence[Hotels] = [Hotels(**hotel.model_dump()) for hotel in hotels]

        session.add_all(new_hotel_objs)
        await session.flush()

        new_hotel_admin_objs = [
            HotelAdmins(hotel_id=obj.id, bot_hashed_password=bcrypt.hashpw(f"password_hotel{obj.id}".encode("utf-8"), bcrypt.gensalt()))
            for obj in new_hotel_objs
        ]
        session.add_all(new_hotel_admin_objs)

        return new_hotel_objs

    @staticmethod
    async def admin_edit_hotel_info(hotel_id: int, session: AsyncSession, info_to_edit: HotelEditSchema) -> Hotels | None:

        if not info_to_edit:
            return None
        
        query = update(Hotels).where(Hotels.id == hotel_id, Hotels.deleted_at.is_(None))
        filters = {}

        if info_to_edit.country:
            filters['country'] = info_to_edit.country

        if info_to_edit.city:
            filters['city'] = info_to_edit.city

        if info_to_edit.rating:
            filters['rating'] = info_to_edit.rating

        if info_to_edit.name:
            filters['name'] = info_to_edit.name

        query = query.values(**filters)
        result = await session.execute(query)
        edited_hotel = result.scalar_one_or_none()

        return edited_hotel


class AdminBotHotelRepo:
    @staticmethod
    async def bot_login(session: AsyncSession, login_info: HotelLoginSchema) -> HotelAdmins | None:
        query = update(HotelAdmins).where(HotelAdmins.hotel_id == login_info.hotel_id).values(chat_id=login_info.chat_id).returning(HotelAdmins)

        result = await session.execute(query)
        updated_info = result.scalar_one_or_none()

        return updated_info

    @staticmethod
    async def bot_logout(session: AsyncSession, hotel_id: int) -> HotelAdmins | None:
        query = update(HotelAdmins).where(HotelAdmins.hotel_id == hotel_id).values(chat_id=None).returning(HotelAdmins)

        result = await session.execute(query)
        updated_info = result.scalar_one_or_none()

        return updated_info

    @staticmethod
    async def get_hotel_admin_info(hotel_id: int, session: AsyncSession) -> HotelAdmins | None:
        query = select(HotelAdmins).where(HotelAdmins.hotel_id == hotel_id).with_for_update()

        result = await session.execute(query)
        hotel = result.scalar_one_or_none()

        return hotel

    @staticmethod
    async def get_hotel_info_by_chat_id(chat_id: str, session: AsyncSession) -> HotelAdmins | None:
        query = select(HotelAdmins).where(HotelAdmins.chat_id == chat_id).with_for_update()

        result = await session.execute(query)
        hotel = result.scalar_one_or_none()

        if hotel:
            return hotel

        return None
