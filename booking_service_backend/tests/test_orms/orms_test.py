# import datetime
# import os

# import pytest
# import pytest_asyncio
# from sqlalchemy.ext.asyncio import (
#     AsyncEngine,
#     AsyncSession,
#     async_sessionmaker,
#     create_async_engine,
# )
# from sqlalchemy.pool import StaticPool

# from app.models.base import Base
# from app.orms.bookings_orm import BookingsOrm
# from app.orms.clients_orm import UsersOrm
# from app.orms.hotels_orm import HotelsOrm
# from app.orms.rooms_orm import RoomsOrm
# from app.schemas.bookings_schemas import BookingsSchema, BookingStatus
# from app.schemas.clients_schemas import UsersSchema
# from app.schemas.hotels_schemas import HotelsSchema
# from app.schemas.rooms_schemas import RoomsSchema
# from app.utils.room_search_filter import RoomSearchFilters


# @pytest_asyncio.fixture
# async def session(async_engine: AsyncEngine) -> AsyncSession:
#     async_session = async_sessionmaker(async_engine, expire_on_commit=False)
#     async with async_session() as session:
#         yield session
#         await session.rollback()


# @pytest.mark.asyncio
# async def test_clients_orm_crud_operations(session: AsyncSession):
#     client_dto = UsersSchema(id=1, full_name="John Doe", phone_number="+10000000000")
#     await UsersOrm.create(client_dto, session)
#     await session.commit()

#     fetched = await UsersOrm.find_by_id(1, session)
#     assert fetched is not None
#     assert fetched.full_name == "John Doe"

#     fetched_by_phone = await UsersOrm.find_by_phone_number("+10000000000", session)
#     assert fetched_by_phone is not None
#     assert fetched_by_phone.id == fetched.id

#     # multi_create + multi_find_by_ids
#     dto_list = [
#         UsersSchema(id=2, full_name="Alice", phone_number="+10000000001"),
#         UsersSchema(id=3, full_name="Bob", phone_number="+10000000002"),
#     ]
#     await UsersOrm.multi_create(dto_list, session)
#     await session.commit()

#     found = await UsersOrm.multi_find_by_ids([2, 3], session)
#     assert {c.id for c in found} == {2, 3}

#     by_name = await UsersOrm.find_by_name("Ali", session)
#     assert len(by_name) == 1
#     assert by_name[0].id == 2

#     deleted = await UsersOrm.delete_by_id(1, session)
#     assert deleted.id == 1
#     await session.commit()

#     assert (await UsersOrm.find_by_id(1, session)) is None


# @pytest.mark.asyncio
# async def test_hotels_and_rooms_orm_basic_crud(session: AsyncSession):
#     hotel_dto = HotelsSchema(name="Test Hotel", country="Wonderland", city="Magic", rating=5)
#     await HotelsOrm.create(hotel_dto, session)
#     await session.commit()

#     hotel = await HotelsOrm.find_by_id(1, session)
#     assert hotel is not None
#     assert hotel.name == "Test Hotel"

#     room_dto = RoomsSchema(hotel_id=hotel.id, category="lux", capacity=2, price_per_night=100)
#     await RoomsOrm.create(room_dto, session)
#     await session.commit()

#     room = await RoomsOrm.find_by_id(1, session)
#     assert room is not None
#     assert room.price_per_night == 100

#     price = await RoomsOrm.get_price_per_night(1, session)
#     assert price == 100

#     found_by_filters = await RoomsOrm.find_room_by_filters(
#         RoomSearchFilters(
#             country="Wonderland",
#             city="Magic",
#             category="lux",
#             min_capacity=2,
#             max_capacity=2,
#             min_price=100,
#             max_price=100,
#         ),
#         session,
#     )
#     assert len(found_by_filters) == 1

#     deleted_room = await RoomsOrm.delete_by_id(1, session)
#     assert deleted_room.id == 1

#     with pytest.raises(ValueError):
#         await RoomsOrm.delete_by_id(1, session)


# @pytest.mark.asyncio
# async def test_bookings_orm_and_availability(session: AsyncSession):
#     # Setup hotel / room / client
#     hotel_dto = HotelsSchema(name="Book Hotel", country="Nowhere", city="Nocity", rating=3)
#     await HotelsOrm.create(hotel_dto, session)
#     await session.commit()

#     room_dto = RoomsSchema(hotel_id=1, category="standart", capacity=1, price_per_night=50)
#     await RoomsOrm.create(room_dto, session)
#     await session.commit()

#     client_dto = UsersSchema(id=10, full_name="Client A", phone_number="+19999999999")
#     await UsersOrm.create(client_dto, session)
#     await session.commit()

#     check_in = datetime.datetime.now() + datetime.timedelta(days=2)
#     check_out = check_in + datetime.timedelta(days=2)

#     booking_dto = BookingsSchema(
#         room_id=1,
#         client_id=10,
#         check_in=check_in,
#         check_out=check_out,
#         total_price=100,
#         status=BookingStatus.booked,
#     )

#     booking_id = await BookingsOrm.new_booking(booking_dto, session)
#     assert booking_id is not None

#     fetched = await BookingsOrm.find_by_id(booking_id, session)
#     assert fetched is not None
#     assert fetched.client_id == 10

#     available = await BookingsOrm.check_is_available(
#         room_id=1,
#         check_in=check_in + datetime.timedelta(hours=1),
#         check_out=check_out - datetime.timedelta(hours=1),
#         session=session,
#     )
#     assert available is False

#     found_by_client = await BookingsOrm.find_by_client_id(10, session)
#     assert found_by_client is not None

#     found_by_room = await BookingsOrm.find_by_room_id(1, session)
#     assert found_by_room is not None

#     found_by_hotel = await BookingsOrm.find_by_hotel_id(1, session)
#     assert found_by_hotel is not None

#     multi = await BookingsOrm.multi_find_by_ids([booking_id], session)
#     assert len(multi) == 1
