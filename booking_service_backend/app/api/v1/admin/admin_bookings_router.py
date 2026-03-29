from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt_gen import get_current_admin_user, get_current_user
from app.models.booking import Bookings
from app.repo.bookings_repo import AdminBookingsRepo
from app.schemas.bookings_schemas import (
    AvailabilityForBookingRequestSchema,
    AvailabilityForBookingResponseSchema,
    BookingsPreparationSchema,
    BookingsResponseSchema,
    ChangeBookingStatusSchema,
    BookingStatsResponseSchema,
    BookingsStatsRequestSchema
)
from app.services.booking_service import BookingService
from app.settings.database import get_db
from app.utils.response_parser import create_booking_response

booking_service = BookingService()

admin_bookings_router = APIRouter(prefix="/admin/bookings", tags=["Admin"], dependencies=[Depends(get_current_admin_user)])


@admin_bookings_router.get("/{booking_id}", summary="Get booking by id (Admin)", response_model=BookingsResponseSchema)
async def admin_get_booking_by_id(booking_id: int, session: AsyncSession = Depends(get_db)) -> BookingsResponseSchema | None:
    booking: Bookings | None = await AdminBookingsRepo.admin_find_by_id(session=session, booking_id=booking_id)

    if booking:
        return create_booking_response(booking)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking with id {booking_id} was not found")


@admin_bookings_router.patch("/{booking_id}/status", summary="Change booking status (Admin)", response_model=BookingsResponseSchema)
async def admin_change_booking_status(booking_id: int, new_status: str = Query(), session: AsyncSession = Depends(get_db)) -> BookingsResponseSchema | None:
    booking: Bookings | None = await AdminBookingsRepo.admin_change_booking_status(booking_id=booking_id, new_status=new_status, session=session)

    if booking:
        return create_booking_response(booking)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking with id {booking_id} was not found")


@admin_bookings_router.delete("/{booking_id}", summary="Delete booking by id (Admin)", response_model=BookingsResponseSchema)
async def admin_delete_booking_by_id(booking_id: int, session: AsyncSession = Depends(get_db)) -> BookingsResponseSchema:
    deleted_booking: Bookings | None = await AdminBookingsRepo.admin_delete_booking(session=session, booking_id=booking_id)

    if deleted_booking:
        return create_booking_response(deleted_booking)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Booking with id {booking_id} was not found")


@admin_bookings_router.get("/stats", summary="Get bookings start by period, rooms, hotels (Admin)", tags=['Admin Analytics'], response_model=BookingStatsResponseSchema)
async def get_booking_stats(filters: Annotated[BookingsStatsRequestSchema, Query()], session: AsyncSession = Depends(get_db)) -> BookingStatsResponseSchema:
    bookings_stats: BookingsResponseSchema | None = await AdminBookingsRepo.admin_get_bookings_stats(filters=filters, session=session)

    if bookings_stats:
        return bookings_stats
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nothing found by filters")