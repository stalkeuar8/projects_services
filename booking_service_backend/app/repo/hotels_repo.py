from typing import Any, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from app.models.booking import Bookings
from app.models.hotel import Hotels, HotelAdmins
from app.repo.base_admin_repo import BaseAdminRepo
from app.repo.base_repo import BaseRepo
from app.schemas.hotels_schemas import HotelEditSchema, HotelSearchFilters
from app.schemas.auth.hotel_bot_schemas import HotelLoginSchema

class HotelsRepo(BaseRepo[Hotels]):
    model = Hotels

    @staticmethod
    async def find_hotel_by_filters(filters: HotelSearchFilters, session: AsyncSession) -> Sequence[Hotels] | None:

        query = select(Hotels).where(Hotels.deleted_at == None)

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

    @staticmethod
    async def admin_edit_hotel_info(hotel_id: int, session: AsyncSession, info_to_edit: HotelEditSchema) -> Hotels | None:
        query = update(Hotels).where(Hotels.id == hotel_id, Hotels.deleted_at == None)

        if info_to_edit.country:
            query = query.values(country=info_to_edit.country)

        if info_to_edit.city:
            query = query.values(city=info_to_edit.city)

        if info_to_edit.rating:
            query = query.values(rating=info_to_edit.rating)

        if info_to_edit.name:
            query = query.values(name=info_to_edit.name)

        result = await session.execute(query)
        edited_hotel = result.scalar()

        return edited_hotel



class AdminBotHotelRepo:
    

    @staticmethod
    async def bot_login(session: AsyncSession, login_info: HotelLoginSchema) -> HotelAdmins | None:
        query = (
            update(HotelAdmins)
            .where(HotelAdmins.hotel_id==login_info.hotel_id)
            .values(chat_id=login_info.chat_id)
            .returning(HotelAdmins)
        )

        result = await session.execute(query)
        updated_info = result.scalar()

        return updated_info
    

    @staticmethod
    async def get_hotel_admin_info(hotel_id: int, session: AsyncSession) -> HotelAdmins | None:
        query = (
            select(HotelAdmins)
            .where(HotelAdmins.hotel_id==hotel_id)
            .with_for_update(nowait=True)
        )

        result = await session.execute(query)   
        hotel = result.scalar()

        return hotel