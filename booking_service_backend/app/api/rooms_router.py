from typing import Annotated, Any, Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hotel import Rooms
from app.repo.rooms_repo import RoomsRepo
from app.schemas.rooms_schemas import RoomCategory, RoomsCreateSchema, RoomSearchFilters, RoomsListResponseSchema, RoomsResponseSchema
from app.settings.database import get_db

rooms_router = APIRouter(prefix="/rooms", tags=["Rooms"])


@rooms_router.get("/", summary="Get rooms by filters", response_model=RoomsListResponseSchema)
async def get_rooms_by_filters(body: Annotated[RoomSearchFilters, Query()], session: AsyncSession = Depends(get_db)) -> RoomsListResponseSchema:
    rooms: Sequence[Rooms] | None = await RoomsRepo.find_room_by_filters(filters=body, session=session)

    if rooms:
        return RoomsListResponseSchema(rooms=rooms)
    
    return RoomsListResponseSchema(rooms=[], total=0)


@rooms_router.get("/{room_id}", summary="Get rooms by filters", response_model=RoomsResponseSchema)
async def get_room_by_id(room_id: int, session: AsyncSession = Depends(get_db)) -> RoomsResponseSchema | None:
    room: Rooms | None = await RoomsRepo.fing_by_id(id_to_find=room_id, session=session)

    if room:
        return RoomsResponseSchema(
            id=room.id,
            hotel_id=room.hotel_id,
            capacity=room.capacity,
            price_per_night=room.price_per_night,
            category=RoomCategory(room.category),
        )

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with id {room_id} was not found")


@rooms_router.post("/", summary="Create room", response_model=RoomsResponseSchema)
async def create_room(body: RoomsCreateSchema, session: AsyncSession = Depends(get_db)) -> RoomsResponseSchema | None:
    new_room: Rooms | None = await RoomsRepo.create(session=session, inserting_data_dto=body)

    if new_room:
        return RoomsResponseSchema(
            id=new_room.id,
            hotel_id=new_room.hotel_id,
            capacity=new_room.capacity,
            price_per_night=new_room.price_per_night,
            category=RoomCategory(new_room.category),
        )

    raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Client not created, Back-end error.")


@rooms_router.delete("/{room_id}", summary="Delete room by id", response_model=RoomsResponseSchema)
async def delete_room_by_id(room_id: int, session: AsyncSession = Depends(get_db)) -> RoomsResponseSchema | None:
    deleted_room: Rooms | None = await RoomsRepo.delete_by_id(session=session, id_to_delete=room_id)

    if deleted_room:
        return RoomsResponseSchema(
            id=deleted_room.id,
            hotel_id=deleted_room.hotel_id,
            capacity=deleted_room.capacity,
            price_per_night=deleted_room.price_per_night,
            category=RoomCategory(deleted_room.category),
        )

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with id {room_id} was not found")
