from datetime import datetime
from typing import Annotated, Any, Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.response_parser import create_room_response
from app.api.v1.bookings_router import booking_service
from app.models.hotel import Rooms
from app.repo.bookings_repo import BookingsRepo
from app.repo.rooms_repo import RoomsRepo
from app.schemas.bookings_schemas import AvailabilityForBookingRequestSchema, AvailabilityForBookingResponseSchema
from app.schemas.rooms_schemas import RoomCategory, RoomsCreateSchema, RoomSearchFilters, RoomsListResponseSchema, RoomsResponseSchema
from app.settings.database import get_db

rooms_router = APIRouter(prefix="/rooms", tags=["Rooms"])


@rooms_router.get("/", summary="Get rooms by filters", response_model=RoomsListResponseSchema)
async def get_rooms_by_filters(body: Annotated[RoomSearchFilters, Query()], session: AsyncSession = Depends(get_db)) -> RoomsListResponseSchema:
    try:
        rooms: Sequence[Rooms] | None = await booking_service.search_matching_rooms(filters=body, session=session)

        if rooms:
            return RoomsListResponseSchema(rooms=rooms, total=len(rooms))

        return RoomsListResponseSchema(rooms=[], total=0)

    except ValueError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Must be or both date limits, or no date limits")


@rooms_router.get("/{room_id}", summary="Get room by id", response_model=RoomsResponseSchema)
async def get_room_by_id(room_id: int, session: AsyncSession = Depends(get_db)) -> RoomsResponseSchema | None:
    room: Rooms | None = await RoomsRepo.find_by_id(id_to_find=room_id, session=session)

    if room:
        return create_room_response(room_obj=room)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with id {room_id} was not found")


@rooms_router.get("/{room_id}/available", summary="Check room availablitity by id and dates", response_model=AvailabilityForBookingResponseSchema)
async def check_room_availability(
    room_id: int, check_in: datetime = Query(), check_out: datetime = Query(), session: AsyncSession = Depends(get_db)
) -> AvailabilityForBookingResponseSchema | None:
    availability_result: bool | None = await BookingsRepo.check_is_available(room_id=room_id, check_in=check_in, check_out=check_out, session=session)

    if availability_result is not None:
        return AvailabilityForBookingResponseSchema(room_id=room_id, check_in=check_in, check_out=check_out, is_available=availability_result)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with id {room_id} was not found")


