from app.models.hotel import Hotels
from app.repo.base_repo import BaseRepo
from app.schemas.hotels_schemas import HotelSearchFilters

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence, Any


class HotelsRepo(BaseRepo[Hotels]):
    model = Hotels

    @staticmethod
    async def find_hotel_by_filters(filters: HotelSearchFilters, session: AsyncSession) -> Sequence[Hotels | None]:

        query = select(Hotels)

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
