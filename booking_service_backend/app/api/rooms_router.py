from typing import Annotated, Sequence, Any

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hotel import Rooms
from app.orms.rooms_orm import RoomsOrm
from app.schemas.rooms_schemas import RoomsResponseSchema, RoomsListResponse
from app.settings.database import get_db
from app.utils.room_search_filter import RoomSearchFilters

rooms_router = APIRouter(prefix="/rooms", tags=["Rooms"])


@rooms_router.get("/", summary="Get rooms by filters", response_model=RoomsListResponse)
async def get_rooms_by_filters(filters: Annotated[RoomSearchFilters, Query()], session: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    rooms: Sequence[Rooms] | None = await RoomsOrm.find_room_by_filters(filters=filters, session=session)

    if rooms:
        return {
            "rooms" : rooms,
            "total" : None
        }

    return {"rooms": [], "total": 0}



@rooms_router.get("/{room_id}", summary="Get rooms by filters", response_model=RoomsResponseSchema)
async def get_room_by_id(room_id: int, session: AsyncSession = Depends(get_db)) -> Rooms:
    room: Rooms | None = await RoomsOrm.fing_by_id(id_to_find=room_id, session=session)
    
    if room:
        return {
            **RoomsResponseSchema(
                hotel_id=room.hotel_id,
                capacity=room.capacity,
                price_per_night=room.price_per_night,
                category=room.category
            ).model_dump()
        }

    raise HTTPException(status_code=404, detail=f"Room with id {room_id} was not found")


@rooms_router.post("/", summary="Create room", response_model=RoomsResponseSchema)