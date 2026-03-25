from typing import Annotated, Any, Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hotel import Rooms
from app.repo.rooms_repo import RoomsRepo
from app.schemas.rooms_schemas import RoomCategory, RoomsCreateSchema, RoomsListResponse, RoomsResponseSchema, RoomSearchFilters
from app.settings.database import get_db

rooms_router = APIRouter(prefix="/rooms", tags=["Rooms"])


@rooms_router.get("/", summary="Get rooms by filters", response_model=RoomsListResponse)
async def get_rooms_by_filters(body: Annotated[RoomSearchFilters, Query()], session: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    rooms: Sequence[Rooms] | None = await RoomsRepo.find_room_by_filters(filters=body, session=session)

    if rooms:
        return {"rooms": rooms, "total": None}

    return {"rooms": [], "total": 0}


@rooms_router.get("/{room_id}", summary="Get rooms by filters", response_model=RoomsResponseSchema)
async def get_room_by_id(room_id: int, session: AsyncSession = Depends(get_db)) -> dict[str, Any] | None:
    room: Rooms | None = await RoomsRepo.fing_by_id(id_to_find=room_id, session=session)

    if room:
        response_obj = RoomsResponseSchema(
            id=room.id,
            hotel_id=room.hotel_id,
            capacity=room.capacity,
            price_per_night=room.price_per_night,
            category=RoomCategory(room.category),
        )

        return {**response_obj.model_dump()}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with id {room_id} was not found")


@rooms_router.post("/", summary="Create room", response_model=RoomsResponseSchema)
async def create_room(body: RoomsCreateSchema, session: AsyncSession = Depends(get_db)) -> dict[str, Any] | None:
    new_room: Rooms | None = await RoomsRepo.create(session=session, inserting_data_dto=body)

    if new_room:
        response_obj = RoomsResponseSchema(
            id=new_room.id,
            hotel_id=new_room.hotel_id,
            capacity=new_room.capacity,
            price_per_night=new_room.price_per_night,
            category=RoomCategory(new_room.category),
        )

        return {**response_obj.model_dump()}

    raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Client not created, Back-end error.")


@rooms_router.delete("/{room_id}", summary="Delete room by id", response_model=RoomsResponseSchema)
async def delete_room_by_id(room_id: int, session: AsyncSession = Depends(get_db)) -> dict[str, Any] | None:
    deleted_room: Rooms | None = await RoomsRepo.delete_by_id(session=session, id_to_delete=room_id)

    if deleted_room:
        response_obj = RoomsResponseSchema(
            id=deleted_room.id,
            hotel_id=deleted_room.hotel_id,
            capacity=deleted_room.capacity,
            price_per_night=deleted_room.price_per_night,
            category=RoomCategory(deleted_room.category),
        )

        return {**response_obj.model_dump()}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with id {room_id} was not found")
