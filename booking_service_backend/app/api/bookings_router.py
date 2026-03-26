from typing import Any, Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Bookings
from app.repo.bookings_repo import BookingsRepo
from app.schemas.bookings_schemas import BookingsPreparationSchema, BookingsResponseSchema, BookingAvailabilityResponseSchema, BookingAvailabilityRequestSchema
from app.services.booking_service import BookingService
from app.settings.database import get_db


booking_service = BookingService()

bookings_router = APIRouter(prefix="/bookings", tags=["Bookings"])


@bookings_router.post("/", summary="Create booking", response_model=BookingsResponseSchema)
async def create_booking(body: BookingsPreparationSchema, session: AsyncSession = Depends(get_db)) -> BookingsResponseSchema | None:
    new_booking: Bookings | None = await booking_service.new_booking(dto=body, session=session)

    if new_booking:
        return BookingsResponseSchema(
            id=new_booking.id,
            room_id=new_booking.room_id,
            client_id=new_booking.client_id,
            created_at=new_booking.created_at,
            check_in=new_booking.check_in,
            check_out=new_booking.check_out,
            total_price=new_booking.total_price,
        )


    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Room is not available for dates {body.check_in}-{body.check_out}")


@bookings_router.get("/{booking_id}", summary="Get booking by id", response_model=BookingsResponseSchema)
async def get_booking_by_id(booking_id: int, session: AsyncSession = Depends(get_db)) -> BookingsResponseSchema | None:
    booking: Bookings | None = await BookingsRepo.fing_by_id(session=session, id_to_find=booking_id)

    if booking:
        return BookingsResponseSchema(
            id=booking.id,
            room_id=booking.room_id,
            client_id=booking.client_id,
            created_at=booking.created_at,
            check_in=booking.check_in,
            check_out=booking.check_out,
            total_price=booking.total_price
        )
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking with id {booking_id} was not found")



@bookings_router.get("/available", summary="Check room availability", response_model=BookingAvailabilityResponseSchema)
async def check_room_availablity(params: Annotated[BookingAvailabilityRequestSchema, Query()], session: AsyncSession = Depends(get_db)) -> BookingAvailabilityResponseSchema | None:    
    availability_result: bool | None = await booking_service.check_available(session=session, dto=params)

    if availability_result is not None:

        return BookingAvailabilityResponseSchema(
            **params.model_dump(),
            is_available=availability_result
        )
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with id {params.room_id} was not found")
