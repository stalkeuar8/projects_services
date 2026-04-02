from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt_gen import get_current_admin_user
from app.models.hotel import Rooms
from app.repo.rooms_repo import AdminRoomsRepo
from app.schemas.rooms_schemas import RoomEditSchema, RoomsCreateSchema, RoomsResponseSchema
from app.settings.database import get_db

admin_rooms_router = APIRouter(prefix="/v1/admin/rooms", tags=["Admin"], dependencies=[Depends(get_current_admin_user)])


@admin_rooms_router.get("/{hotel_id}", summary="Get room by id (Admin)", response_model=RoomsResponseSchema)
async def admin_get_room_by_id(hotel_id: int, session: AsyncSession = Depends(get_db)) -> RoomsResponseSchema | None:
    hotel: Rooms | None = await AdminRoomsRepo.admin_find_by_id(id_to_find=hotel_id, session=session)

    if hotel:
        return RoomsResponseSchema.model_validate(hotel)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with id {hotel_id} was not found")


@admin_rooms_router.post("/", summary="Create room (Admin)", response_model=RoomsResponseSchema)
async def admin_create_room(body: RoomsCreateSchema, session: AsyncSession = Depends(get_db)) -> RoomsResponseSchema | None:
    new_room: Rooms | None = await AdminRoomsRepo.create(session=session, inserting_data_dto=body)

    if new_room:
        return RoomsResponseSchema.model_validate(new_room)

    raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Client not created, Back-end error.")


@admin_rooms_router.post("/massive", summary="Multi create room (Admin)", response_model=Sequence[RoomsResponseSchema])
async def admin_multi_create_room(body: list[RoomsCreateSchema], session: AsyncSession = Depends(get_db)) -> Sequence[RoomsResponseSchema]:
    new_rooms: Sequence[Rooms] | None = await AdminRoomsRepo.multi_create(session=session, inserting_data_list_dto=body)

    if new_rooms:
        return [RoomsResponseSchema.model_validate(room) for room in new_rooms]

    raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Client not created, Back-end error.")


@admin_rooms_router.delete("/{room_id}", summary="Delete room by id (Admin)", response_model=RoomsResponseSchema)
async def admin_delete_room_by_id(room_id: int, session: AsyncSession = Depends(get_db)) -> RoomsResponseSchema | None:
    deleted_room: Rooms | None = await AdminRoomsRepo.admin_delete_by_id(session=session, id_to_delete=room_id)

    if deleted_room:
        return RoomsResponseSchema.model_validate(deleted_room)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with id {room_id} was not found")


@admin_rooms_router.patch("/{room_id}", summary="Edit room info (Admin)", response_model=RoomsResponseSchema)
async def edit_room_info(room_id: int, body: RoomEditSchema, session: AsyncSession = Depends(get_db)) -> RoomsResponseSchema:
    edited_room: Rooms | None = await AdminRoomsRepo.admin_edit_room_info(room_id=room_id, session=session, info_to_edit=body)

    if edited_room:
        return RoomsResponseSchema.model_validate(edited_room)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Room with id {room_id} was not found")
