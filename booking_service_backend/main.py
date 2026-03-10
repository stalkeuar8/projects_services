from app.orms.base_orm import create_tables
from app.orms.bookings_orm import BookingsOrm
from app.orms.hotels_orm import HotelsOrm
from app.orms.clients_orm import ClientsOrm
from app.orms.rooms_orm import RoomsOrm
from app.utils.room_search_filter import RoomSearchFilters
from app.services.booking_service import BookingService
from app.models.hotel import Rooms
import asyncio

async def main():

    await create_tables()

    filters = {
        "country" : "Switzerland",
        "min_rating" : 4,
        "max_rating" : 5,
        "min_price" : 10000,
        "max_price" : 20000
    }
    
    booking_service = BookingService()
    rooms: list[Rooms] = await booking_service.search_matching_rooms(
        filters=RoomSearchFilters(**filters)
    )
    if rooms:
        for room in rooms:
            print(room.hotel.name, room.id, room.price_per_night)


if __name__ == '__main__':
    asyncio.run(main())