from app.models.booking import Bookings, Clients
from app.models.hotel import Hotels, Rooms
from app.utils.room_search_filter import RoomSearchFilters
from app.orms.bookings_orm import BookingsOrm
from app.orms.hotels_orm import HotelsOrm
from app.orms.rooms_orm import RoomsOrm
from app.orms.clients_orm import ClientsOrm
from app.utils.transaction_deco import transaction
from app.services.base_service import BaseService
from app.schemas.bookings_schemas import BookingCreateDTO
from sqlalchemy.ext.asyncio import AsyncSession

# MAKE BASE SERVICE AND INHERIT!!!

class BookingService(BaseService):

    @transaction
    async def search_matching_rooms(self, filters: RoomSearchFilters, session: AsyncSession = None):
        print(f"Finding matching rooms by filters: {filters.model_dump(exclude_none=True)}")

        rooms = await RoomsOrm.find_room_by_filters(filters=filters, session=session)

        return rooms
    

    @transaction 
    async def check_available(self, dto: BookingCreateDTO, session: AsyncSession = None):
        room_id = dto.room_id
        check_in = dto.check_in
        check_out = dto.check_out
        
        room_info: Bookings = BookingsOrm.check_room_status(room_id=room_id, session=session)

        if room_info:

            if room_info.check_out and check_in > room_info.check_out:
                new_booking = BookingsOrm.new_booking()

