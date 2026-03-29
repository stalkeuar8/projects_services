from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt_gen import get_current_user
from app.models.booking import Bookings
from app.models.user import Users
from app.repo.bookings_repo import BookingsRepo
from app.schemas.bookings_schemas import (
    AvailabilityForBookingRequestSchema,
    AvailabilityForBookingResponseSchema,
    BookingsPreparationSchema,
    BookingsResponseSchema,
)
from app.services.booking_service import BookingService
from app.settings.database import get_db
from app.utils.response_parser import create_booking_response

booking_service = BookingService()

bookings_router = APIRouter(prefix="/bookings", tags=["Bookings"])


@bookings_router.get("/", summary="Get all user bookings (Only bookings created by current user)", response_model=BookingsResponseSchema)
async def get_booking_by_id(session: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)) -> BookingsResponseSchema:
    booking: Bookings | None = await BookingsRepo.find_all_my_bookings(session=session, current_user_id=current_user.id)

    if booking:
        return create_booking_response(booking)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bookings was not found")


@bookings_router.get("/{booking_id}", summary="Get booking by id (Only bookings created by current user)", response_model=BookingsResponseSchema)
async def get_booking_by_id(
    booking_id: int, session: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)
) -> BookingsResponseSchema:
    booking: Bookings | None = await BookingsRepo.find_my_booking_by_id(session=session, id_to_find=booking_id, current_user_id=current_user.id)

    if booking:
        return create_booking_response(booking)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking with id {booking_id} was not found")



@bookings_router.post("/", summary="Create booking (Only logined users)", response_model=BookingsResponseSchema)
async def create_booking(
    body: BookingsPreparationSchema, session: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)
) -> BookingsResponseSchema:
    new_booking: Bookings | None = await booking_service.new_booking(user_id=current_user.id, dto=body, session=session)

    if new_booking:
        return BookingsResponseSchema(
            **body.model_dump(),
            user_id=current_user.id,
            id=new_booking.id,
            created_at=new_booking.created_at,
            total_price=new_booking.total_price,
        )

    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Room is not available for dates {body.check_in}-{body.check_out}")


@bookings_router.patch("/{booking_id}/cancel", summary="Cancel user booking by id (Only logined users)", response_model=BookingsResponseSchema)
async def cancel_booking_by_id(booking_id: int, current_user: Users = Depends(get_current_user), session: AsyncSession = Depends(get_db)) -> BookingsResponseSchema:
    canceled_booking: Bookings | None = await BookingsRepo.cancel_my_booking_by_id(booking_id=booking_id, session=session, current_user_id=current_user.id)

    if canceled_booking:
        return create_booking_response(booking_obj=canceled_booking)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking with id {booking_id} was not found") 

# # THINK ABOUT!!!
# @bookings_router.get("/{room_id}/available", summary="Check room availability", response_model=AvailabilityForBookingRequestSchema)
# async def check_room_availablity(
#     params: Annotated[AvailabilityForBookingRequestSchema, Query()], session: AsyncSession = Depends(get_db)
# ) -> AvailabilityForBookingResponseSchema | None:
#     availability_result: bool | None = await booking_service.check_available(session=session, dto=params)

#     if availability_result is not None:
#         return AvailabilityForBookingResponseSchema(**params.model_dump(), is_available=availability_result)

#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with id {params.room_id} was not found")
