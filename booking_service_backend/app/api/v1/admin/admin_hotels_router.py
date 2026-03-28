from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.response_parser import create_hotel_response
from app.models.hotel import Hotels
from app.repo.hotels_repo import HotelsRepo
from app.schemas.hotels_schemas import HotelsCreateSchema, HotelEditSchema, HotelSearchFilters, HotelsListResponseSchema, HotelsResponseSchema
from app.settings.database import get_db
from app.auth.jwt_gen import get_current_admin_user


admin_hotels_router = APIRouter(prefix="/admin/hotels", tags=['Admin'], dependencies=[Depends(get_current_admin_user)])


@admin_hotels_router.post("/", summary="Create hotel (Admin)", response_model=HotelsResponseSchema)
async def admin_create_hotel(body: HotelsCreateSchema, session: AsyncSession = Depends(get_db)) -> HotelsResponseSchema:
    new_hotel: Hotels | None = await HotelsRepo.create(session=session, inserting_data_dto=body)

    if new_hotel:
        return create_hotel_response(hotel_obj=new_hotel)

    raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Hotel not created, Back-end error.")


@admin_hotels_router.delete("/{hotel_id}", summary="Delete hotel by id (Admin)", response_model=HotelsResponseSchema)
async def admin_delete_hotel_by_id(hotel_id: int, session: AsyncSession = Depends(get_db)) -> HotelsResponseSchema | None:
    deleted_hotel: Hotels | None = await HotelsRepo.delete_by_id(session=session, id_to_delete=hotel_id)

    if deleted_hotel:
        return create_hotel_response(hotel_obj=deleted_hotel)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with id {hotel_id} was not found")


@admin_hotels_router.patch("/{hotel_id}", summary="Edit hotel info (Admin)", response_model=HotelsResponseSchema)
async def edit_hotel_info(hotel_id: int, body: HotelEditSchema, session: AsyncSession = Depends(get_db)) -> HotelsResponseSchema:
    edited_hotel: Hotels | None = await HotelsRepo.edit_hotel_info(hotel_id=hotel_id, session=session, info_to_edit=body)

    if edited_hotel:

        return create_hotel_response(edited_hotel)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with id {hotel_id} was not found")