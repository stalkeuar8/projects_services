from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.response_parser import create_booking_response
from app.models.booking import Bookings
from app.repo.bookings_repo import BookingsRepo
from app.schemas.bookings_schemas import (
    AvailabilityForBookingRequestSchema,
    AvailabilityForBookingResponseSchema,
    BookingsPreparationSchema,
    BookingsResponseSchema,
    ChangeBookingStatusSchema
)
from app.services.booking_service import BookingService
from app.settings.database import get_db
from app.auth.jwt_gen import get_current_user, get_current_admin_user


booking_service = BookingService()

admin_bookings_router = APIRouter(prefix="/admin/bookings", tags=['Admin'], dependencies=Depends(get_current_admin_user))


@admin_bookings_router.get("/{booking_id}", summary="Get booking by id (Admin)", response_model=BookingsResponseSchema)
async def admin_get_booking_by_id(booking_id: int, session: AsyncSession = Depends(get_db)) -> BookingsResponseSchema | None:
    booking: Bookings | None = await BookingsRepo.find_by_id(session=session, id_to_find=booking_id)

    if booking:
        return create_booking_response(booking)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking with id {booking_id} was not found")



@admin_bookings_router.patch('/{booking_id}/status', summary="Change booking status (Admin)", response_model=BookingsResponseSchema)
async def admin_change_booking_status(booking_id: int, new_status = Query(), session: AsyncSession = Depends(get_db)) -> BookingsResponseSchema | None:
    booking: Bookings | None =  await BookingsRepo.change_booking_status(booking_id=booking_id, new_status=new_status, session=session)

    if booking:
        return create_booking_response(booking)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking with id {booking_id} was not found")


