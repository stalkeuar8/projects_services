from app.orms.base_orm import create_tables
from app.utils.room_search_filter import RoomSearchFilters
from app.utils.bg_tasks_observer import BackgroundTaskObserver
from app.utils.paginator import ResultsPaginator
from app.services.background_processes import BackgroundProcesses
from app.services.booking_service import BookingService
from app.models.hotel import Rooms
from app.settings.database import async_session_factory
import asyncio
import datetime


async def main():

    bg_coroutines = {
        BackgroundProcesses.background_bookings_cleaner(),
        BackgroundProcesses.background_status_checker()
    }

    async with BackgroundTaskObserver(bg_coroutines) as bg_task_observer:

        filters = RoomSearchFilters(
            country="Switzerland",
            min_rating=4,
            max_rating=5,
            min_price=10000,
            max_price=20000
        )

        async with async_session_factory.begin() as session:
        
            booking_service = BookingService()

            await create_tables()

            rooms: list[Rooms] = await booking_service.search_matching_rooms(filters=filters, session=session)
            paginator = ResultsPaginator(rooms, 10)
            matching_rooms_ids = []
            for i, page in enumerate(paginator, start=1):
                print(f"page {i}")
                for room in page:
                    matching_rooms_ids.append(room.id)
                    print(f"Hotel name: {room.hotel.name}, room id: {room.id}, price per night: {room.price_per_night}")
                print("-----")

            
            room_id = int(input("Enter room id: "))
            if not room_id in matching_rooms_ids:
                raise ValueError("Wrong room id.") # remove after tests
            
            year, month, day = [int(el) for el in input('Enter check in date: ').split('-')]
            check_in = datetime.datetime(year, month, day)
            year, month, day = [int(el) for el in input('Enter check out date: ').split('-')]
            check_out = datetime.datetime(year, month, day)

            print(f"room_id: {room_id}, check-in date: {check_in}, check-out date: {check_out}")

            result = await booking_service.check_available(room_id=room_id, check_in=check_in, check_out=check_out, session=session)
                
            new_booking_id = None

            if result:
                dto = await booking_service.prepare_dto(room_id=room_id, client_id=1, check_in=check_in, check_out=check_out, session=session)
                new_booking_id = await booking_service.new_booking(dto=dto, session=session)

            else: 
                print(f"Sorry, but room {room_id} for dates '{check_in}'-'{check_out}' is not available, check other rooms or change dates!")


        if new_booking_id:

            task_result = asyncio.create_task(booking_service.approve_booking(booking_id=new_booking_id))
            approving_result = await task_result

            if approving_result:
                print(f"Room '{room_id}' successfully booked for dates '{check_in}'-'{check_out}'")
            
            else:
                print(f"Sorry, but hotel canceled your booking '{new_booking_id}' for room {room_id} for dates '{check_in}'-'{check_out}'")
                print("Reason: hotel personal service reasons.")

            

if __name__ == '__main__':
    asyncio.run(main())



    # async def create_tasks(self):
    #     for task in self.inactive_tasks:
    #         self.active_tasks.add(asyncio.create_task(task))
    #     self.inactive_tasks = set()

    # async def cancel_tasks(self):
    #     for task in self.active_tasks:
    #         task.cancel()
    #     self.active_tasks = set()