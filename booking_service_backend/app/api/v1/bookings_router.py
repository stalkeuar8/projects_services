from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

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
from app.auth.jwt_gen import get_current_user

booking_service = BookingService()

bookings_router = APIRouter(prefix="/bookings", tags=["Bookings"])


@bookings_router.post("/", summary="Create booking", response_model=BookingsResponseSchema)
async def create_booking(body: BookingsPreparationSchema, session: AsyncSession = Depends(get_db)) -> BookingsResponseSchema | None:
    new_booking: Bookings | None = await booking_service.new_booking(dto=body, session=session)

    if new_booking:
        return BookingsResponseSchema(
            **body.model_dump(),
            id=new_booking.id,
            created_at=new_booking.created_at,
            total_price=new_booking.total_price,
        )

    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Room is not available for dates {body.check_in}-{body.check_out}")


@bookings_router.get("/{booking_id}", summary="Get booking by id", response_model=BookingsResponseSchema)
async def get_booking_by_id(booking_id: int, session: AsyncSession = Depends(get_db), current_user: Users = Depends(get_current_user)) -> BookingsResponseSchema | None:
    booking: Bookings | None = await BookingsRepo.find_by_id(session=session, id_to_find=booking_id)

    if booking:
        return BookingsResponseSchema(
            id=booking.id,
            room_id=booking.room_id,
            user_id=booking.user_id,
            created_at=booking.created_at,
            check_in=booking.check_in,
            check_out=booking.check_out,
            total_price=booking.total_price,
        )

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
