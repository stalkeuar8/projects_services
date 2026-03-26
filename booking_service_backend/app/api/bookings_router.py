from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Bookings
from app.repo.bookings_repo import BookingsRepo
from app.schemas.bookings_schemas import BookingsCreateSchema, BookingsPreparationSchema, BookingsResponseSchema, BookingStatus
from app.services.booking_service import BookingService
from app.settings.database import get_db

booking_service = BookingService()

bookings_router = APIRouter(prefix="/bookings", tags=["Bookings"])


@bookings_router.post("/", summary="Create booking", response_model=BookingsResponseSchema)
async def create_booking(body: BookingsPreparationSchema, session: AsyncSession = Depends(get_db)) -> dict[str, Any] | None:
    new_booking: Bookings | None = await booking_service.new_booking(dto=body, session=session)

    if new_booking:
        response_obj = BookingsResponseSchema(
            id=new_booking.id,
            room_id=new_booking.room_id,
            client_id=new_booking.client_id,
            created_at=new_booking.created_at,
            check_in=new_booking.check_in,
            check_out=new_booking.check_out,
            total_price=new_booking.total_price,
        )

        return {**response_obj.model_dump()}

    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Room is not available for dates {body.check_in}-{body.check_out}")
