from app.models.hotel import Rooms, Hotels
from app.schemas.rooms_schemas import RoomsSchema
from app.orms.base_orm import BaseOrm
from app.utils.room_search_filter import RoomSearchFilters
from app.utils.transaction_deco import transaction
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager


class RoomsOrm(BaseOrm):

    @transaction
    @staticmethod
    async def create(incoming_data_dto: RoomsSchema, session: AsyncSession | None = None):

        room = Rooms(**incoming_data_dto.model_dump())

        session.add(room)


    @transaction
    @staticmethod
    async def multi_create(incoming_data_list_dto: list[RoomsSchema], session: AsyncSession | None = None):

        rooms = [Rooms(**room.model_dump()) for room in incoming_data_list_dto]

        session.add_all(rooms)


    @transaction
    @staticmethod
    async def find_by_id(id_to_find: int, session: AsyncSession | None = None):
        query = (
            select(Rooms)
            .filter_by(id=id_to_find)
        )
        result = await session.execute(query)
        room = result.scalar_one_or_none()
        return room
    

    @transaction
    @staticmethod
    async def get_price_per_night(id_to_find: int, session: AsyncSession | None = None):
        query = (
            select(Rooms.price_per_night)
            .filter_by(id=id_to_find)
        )
        result = await session.execute(query)
        price = result.first()[0]
        return price


    @transaction
    @staticmethod
    async def find_room_by_filters(filters: RoomSearchFilters, session: AsyncSession = None):
        validated_filters = filters.model_validate(filters)

        query = (
            select(Rooms)
            .join(Rooms.hotel)

        )

        if filters.country:
            query = (
                query
                .where(Hotels.country==filters.country)
                .options(contains_eager(Rooms.hotel))
            )
            
        if filters.city:
            query = (
                query
                .where(Hotels.city==filters.country)
                .options(contains_eager(Rooms.hotel))
            )

        if filters.min_rating and filters.max_rating:
            if filters.min_rating != filters.max_rating:

                if filters.min_rating > filters.max_rating:
                    filters.min_rating, filters.max_rating = filters.max_rating, filters.min_rating
                    
                query = (
                    query
                    .where(Hotels.rating.between(filters.min_rating, filters.max_rating))
                )
            else:
                query = (
                    query
                    .where(Hotels.rating == filters.min_rating)
                )

        elif filters.min_rating:
            query = (
                    query
                    .where((Hotels.rating > filters.min_rating) | (Hotels.rating == filters.min_rating))
                )
            
        elif filters.max_rating:
            query = (
                    query
                    .where((Hotels.rating < filters.max_rating) | (Hotels.rating == filters.max_rating))
                )

        if filters.category:
            query = (
                query
                .filter_by(category=filters.category)
            )


        if filters.min_capacity and filters.max_capacity:
            if filters.min_capacity != filters.max_capacity:

                if filters.min_capacity > filters.max_capacity:
                    filters.min_capacity, filters.max_capacity = filters.max_capacity, filters.min_capacity
                    
                query = (
                    query
                    .where(Rooms.capacity.between(filters.min_capacity, filters.max_capacity))
                )
            else:
                query = (
                    query
                    .where(Rooms.capacity == filters.min_capacity)
                )

        elif filters.min_capacity:
            query = (
                    query
                    .where((Rooms.capacity > filters.min_capacity) | (Rooms.capacity == filters.min_capacity))

                )
            
        elif filters.max_capacity:
            query = (
                    query
                    .where((Rooms.capacity < filters.max_capacity) | (Rooms.capacity == filters.max_capacity))
                )


        if filters.min_price and filters.max_price:
            if filters.min_price != filters.max_price:

                if filters.min_price > filters.max_price:
                    filters.min_price, filters.max_price = filters.max_price, filters.min_price
                    
                query = (
                    query
                    .where(Rooms.price_per_night.between(filters.min_price, filters.max_price))
                )
            else:
                query = (
                    query
                    .where(Rooms.price_per_night == filters.min_price)
                )

        elif filters.min_price:
            query = (
                    query
                    .where((Rooms.price_per_night > filters.min_price) | (Rooms.price_per_night == filters.min_price))
                )
            
        elif filters.max_price:
            query = (
                    query
                    .where((Rooms.price_per_night < filters.max_price) | (Rooms.price_per_night == filters.max_price))

                )
        

        results = await session.execute(query)
        rooms = results.scalars().all()

        return rooms



    @transaction
    @staticmethod
    async def delete_by_id(id_to_delete: int, session: AsyncSession | None = None):
        query = (
            delete(Rooms)
            .where(Rooms.id == id_to_delete)
            .returning(Rooms)
        )
        result = await session.execute(query)
        room_to_delete = result.scalar_one_or_none()

        if not room_to_delete:
            raise ValueError("Room was not found")
            
        return room_to_delete


