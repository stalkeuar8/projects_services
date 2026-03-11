from app.orms.base_orm import create_tables
from app.orms.bookings_orm import BookingsOrm
from app.orms.hotels_orm import HotelsOrm
from app.orms.clients_orm import ClientsOrm
from app.orms.rooms_orm import RoomsOrm
from app.utils.room_search_filter import RoomSearchFilters
from app.services.booking_service import BookingService
from app.models.hotel import Rooms
from app.services.background_processes import BackgroundCleaner
from app.utils.paginator import ResultsPaginator
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
        paginator = ResultsPaginator(rooms, 10)

        for i, page in enumerate(paginator, start=1):
            try:
                page = next(paginator)
                print(f"page {i}")
                for room in page:
                    print(f"Hotel name: {room.hotel.name}, room id: {room.id}, price per night: {room.price_per_night}")
                print("-----")
            except StopIteration as e:
                break 
        
        room_id = int(input("Enter room id: "))
        year, month, day = [int(el) for el in input('Enter check in date: ').split('-')]
        check_in = datetime.datetime(year, month, day)
        year, month, day = [int(el) for el in input('Enter check out date: ').split('-')]
        check_out = datetime.datetime(year, month, day)

        print(f"room_id: {room_id}, check-in date: {check_in}, check-out date: {check_out}")

        result = await booking_service.check_available(room_id, check_in, check_out)
        
        if result:
            dto = await booking_service.prepare_dto(room_id=room_id, client_id=1, check_in=check_in, check_out=check_out)
            new_booking_id = await booking_service.new_booking(dto=dto)
            approving_task = asyncio.create_task(booking_service.approve_booking(booking_id=new_booking_id))
            print(f"Room '{room_id}' successfully booked for dates '{check_in}'-'{check_out}'")
        else: 
            print(f"Sorry, but room {room_id} for dates '{check_in}'-'{check_out}' is not available, check other rooms or change dates!")

    except Exception as e:
        print(e)

if __name__ == '__main__':
    asyncio.run(main())

        # 10189
    # price per night - 11800