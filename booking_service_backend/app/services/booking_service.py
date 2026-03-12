from app.models.booking import Bookings, Clients
from app.models.hotel import Hotels, Rooms
from app.utils.room_search_filter import RoomSearchFilters
from app.orms.bookings_orm import BookingsOrm
from app.orms.hotels_orm import HotelsOrm
from app.orms.rooms_orm import RoomsOrm
from app.orms.clients_orm import ClientsOrm
from app.services.base_service import BaseService
from app.schemas.bookings_schemas import BookingsSchema
from app.settings.database import async_session_factory
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
import datetime
import asyncio
import random 
# MAKE BASE SERVICE AND INHERIT!!!

class BookingService(BaseService):

    async def search_matching_rooms(self, filters: RoomSearchFilters, session: AsyncSession):
        print(f"Finding matching rooms by filters: {filters.model_dump(exclude_none=True)}")

        rooms = await RoomsOrm.find_room_by_filters(filters=filters, session=session)

        return rooms
    

    async def check_available(self, room_id: int, check_in: datetime.datetime, check_out: datetime.datetime, session: AsyncSession):
    
        room_status: Bookings = await BookingsOrm.check_is_available(room_id=room_id, check_in=check_in, check_out=check_out, session=session)
    
        return room_status
            

    async def prepare_dto(self, room_id: int, client_id: int, check_in: datetime.datetime, check_out: datetime.datetime, session: AsyncSession):
        
        price_per_night = await RoomsOrm.get_price_per_night(id_to_find=room_id, session=session)
        total_days = (check_out - check_in).days
        
        dto = BookingsSchema(
            room_id=room_id,
            client_id=client_id,
            check_in=check_in,
            check_out=check_out,
            total_price=total_days * price_per_night,
            status='pending'
        )

        return dto 
    

    async def new_booking(self, dto: BookingsSchema, session: AsyncSession):
         new_booking_id = await BookingsOrm.new_booking(incoming_data_dto=dto, session=session)
         
         return new_booking_id
    


    async def approve_booking(self, booking_id: int):
        print(f"\nApproving....\n")

        time_to_sleep = random.randint(5, 10)
        await asyncio.sleep(time_to_sleep)

        chance = random.randint(1, 100)

        is_successful = None

        if 90 <= chance <= 100:
            query = (
                update(Bookings)
                .values(status='canceled')
                .where(Bookings.id==booking_id)
            )
            is_successful = False

        else:
            query = (
                update(Bookings)
                .values(status='booked')
                .where(Bookings.id==booking_id)
            )
            is_successful = True

        async with async_session_factory() as session:

            await session.execute(query)
            await session.commit()

        return is_successful
        
