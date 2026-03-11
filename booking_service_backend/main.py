from app.orms.base_orm import create_tables
from app.orms.bookings_orm import BookingsOrm
from app.orms.hotels_orm import HotelsOrm
from app.orms.clients_orm import ClientsOrm
from app.orms.rooms_orm import RoomsOrm
from app.utils.room_search_filter import RoomSearchFilters
from app.services.booking_service import BookingService
from app.models.hotel import Rooms
from app.services.background_processes import BackgroundCleaner
import asyncio
import datetime

async def main():

    try:
        
        booking_service = BookingService()

        await create_tables()
        cleaner_task = asyncio.create_task(
            BackgroundCleaner.background_bookings_cleaner(5)
        )

        filters = RoomSearchFilters(
            country="Switzerland",
            min_rating=4,
            max_rating=5,
            min_price=10000,
            max_price=20000
        )
        
        rooms: list[Rooms] = await booking_service.search_matching_rooms(filters=filters)

        room_id = 10189
        check_in = datetime.datetime(2026, 10, 12)
        check_out = datetime.datetime(2026, 10, 17)

        result = await booking_service.check_available(room_id, check_in, check_out)
        
        if result:
            dto = await booking_service.prepare_dto(room_id=room_id, client_id=1, check_in=check_in, check_out=check_out)
            await booking_service.new_booking(dto=dto)
            print(f"Room '{room_id}' successfully booked for dates '{check_in}'-'{check_out}'")
        else: 
            print(f"Sorry, but room {room_id} for dates '{check_in}'-'{check_out}' is not available, check other rooms or change dates!")

    except Exception as e:
        print(e)

if __name__ == '__main__':
    asyncio.run(main())

        # 10189
    # price per night - 11800