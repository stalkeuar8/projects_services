import asyncio
import datetime
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from sqlalchemy.exc import IntegrityError 

from app.api.v1.auth_routers import auth_router
from app.api.v1.bookings_router import bookings_router
from app.api.v1.hotels_router import hotels_router
from app.api.v1.rooms_router import rooms_router
from app.api.v1.users_router import users_router
from app.models.hotel import Rooms
from app.repo.base_repo import create_tables
from app.services.background_processes import BackgroundProcesses
from app.services.booking_service import BookingService
from app.settings.database import async_engine, async_session_factory
from app.utils.paginator import ResultsPaginator

# START FUNCS, ROUTERS


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:
    yield
    await async_engine.dispose()


def create_app() -> FastAPI:

    app = FastAPI(title="Booking Service", lifespan=lifespan)

    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(bookings_router)
    app.include_router(hotels_router)
    app.include_router(rooms_router)
    
    return app


app = create_app()



@app.exception_handler(IntegrityError)
async def handle_integrity_error(request: Request, exc: IntegrityError) -> None:
    error_msg = str(exc.orig)

    error_details = 'Error caused becuase '

    if 'phone_number' in error_msg:
        error_details += f"'phone_number' "
    if "email" in error_msg:
        error_details += f"'email' "
    error_details += ' already exists, must be unique'

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error_msg" : error_msg,
            "details" : error_details
        }
    )

# async def main() -> None:

#     # bg_coroutines = {
#     #     BackgroundProcesses.background_bookings_cleaner(),
#     #     BackgroundProcesses.background_status_checker(),
#     # }

#     # async with BackgroundTaskObserver(bg_coroutines):
#         # filters example (mention only filled filters by user, dont mention empty)
#         # filters = RoomSearchFilters(
#         #     country="some country",
#         #     city="some city",
#         #     min_rating="min value: 1, type: int",
#         #     max_rating="max value: 5, type: int",
#         #     category="available categories: (standard, superior, lux, presidental), type: str",
#         #     min_capacity="min value: 1, max value: 3, type: int",
#         #     max_capacity="min value: 1, max value: 3, must be bigger than min_price, type: int",
#         #     min_price="min value: 1, type: int",
#         #     max_price="min value: 1, must be bigger than min_price, type: int",
#         # )

#         # filters = RoomSearchFilters()

#         async with async_session_factory.begin() as session:
#             booking_service = BookingService()

#             await create_tables()

#             # rooms: list[Rooms] = await booking_service.search_matching_rooms(
#             #     filters=filters, session=session
#             # )

#             # paginator = ResultsPaginator(rooms, 10)

#             # EXAMPLE FOR CLI!!!!
#             # matching_rooms_ids = []
#             # for i, page in enumerate(paginator, start=1):
#             #     print(f"page {i}")
#             #     for room in page:
#             #         matching_rooms_ids.append(room.id)
#             #         print(f"Hotel name: {room.hotel.name}, room id: {room.id}, price per night: {room.price_per_night}")
#             #     print("-----")

#             # EXAMPLE!!! DONT RUN LIKE THIS!!!
#             # incoming_choice_example = {
#             #     "client_id": "1",
#             #     "room_id": "integer",
#             #     "check_in": "datetime",
#             #     "check_out": "datetime",
#             # }
#             incoming_choice_example = {
#                 "client_id": 54,
#                 "room_id": 3565,
#                 "check_in": datetime.datetime(2027, 10, 10, tzinfo=datetime.timezone.utc),
#                 "check_out": datetime.datetime(2027, 10, 20, tzinfo=datetime.timezone.utc),
#             }

#             short_dto_obj = BookingsCheckAvailableSchema(**incoming_choice_example)  # validation and transfer

#             result = await booking_service.check_available(dto=short_dto_obj, session=session)

#             new_booking_id = None

#             if result:
#                 dto = await booking_service.prepare_dto(short_dto=short_dto_obj, session=session)
#                 new_booking_obj = await booking_service.new_booking(dto=dto, session=session)
#                 new_booking_id = new_booking_obj.id

#             else:
#                 # example (remove in prod)
#                 print(f"Sorry, but room {short_dto_obj.room_id} for dates '{short_dto_obj.check_in}'-'{short_dto_obj.check_out}'
#               is not available, check other rooms or change dates!")

#         if new_booking_id:
#             task_result = asyncio.create_task(booking_service.approve_booking(booking_id=new_booking_id))
#             approving_result = await task_result

#             if approving_result:
#                 # example (remove in prod)
#                 print(f"Room '{short_dto_obj.room_id}' successfully booked for dates
#   '{short_dto_obj.check_in}'-'{short_dto_obj.check_out}'")

#             else:
#                 # example (remove in prod)1
#                 print(f"Sorry, but hotel canceled your booking '{new_booking_id}' for room {short_dto_obj.room_id} for
#       dates '{short_dto_obj.check_in}'-'{short_dto_obj.check_out}'")
#                 print("Reason: hotel personal service reasons.")


# if __name__ == "__main__":
#     asyncio.run(main())
