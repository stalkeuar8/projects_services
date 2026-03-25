from typing import Any, Annotated

from fastapi import APIRouter, Depends, Query, status, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.settings.database import get_db
from app.models.hotel import Hotels
from app.repo.hotels_repo import HotelsRepo
from app.schemas.hotels_schemas import HotelSearchFilters, HotelsResponseSchema, HotelsCreateSchema, HotelsListResponseSchema

hotels_router = APIRouter(prefix="/hotels", tags=['Hotels'])


@hotels_router.get("/", summary="Get hotels by filters", response_model=HotelsListResponseSchema)
async def get_hotels_by_filters(body: Annotated[HotelSearchFilters, Query()], session: AsyncSession = Depends(get_db)) -> dict[str, Any] | None:
    hotels: list[Hotels] | None = await HotelsRepo.find_hotel_by_filters(filters=body, session=session)

    if hotels:
        return {"hotels": hotels, "total": None}

    return {"hotels": [], "total": 0}


@hotels_router.get("/{hotel_id}", summary="Get hotel by id", response_model=HotelsResponseSchema) 
async def get_hotel_by_id(hotel_id: int, session: AsyncSession = Depends(get_db)) -> dict[str, Any] | None:
    hotel: Hotels | None = await HotelsRepo.fing_by_id(id_to_find=hotel_id, session=session)

    if hotel:

        response_obj = HotelsResponseSchema(
            id=hotel.id,
            name=hotel.name,
            country=hotel.country,
            city=hotel.city,
            rating=hotel.rating
        )

        return {**response_obj.model_dump()}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with id {hotel_id} was not found")



@hotels_router.post("/", summary="Create hotel", response_model=HotelsResponseSchema)
async def create_hotel(body: HotelsCreateSchema, session: AsyncSession = Depends(get_db)) -> dict[str, Any] | None:
    new_hotel: Hotels | None = await HotelsRepo.create(session=session, inserting_data_dto=body)

    if new_hotel:
        response_obj = HotelsResponseSchema(
            id=new_hotel.id,
            name=new_hotel.name,
            country=new_hotel.country,
            city=new_hotel.city,
            rating=new_hotel.rating
        )

        return {**response_obj.model_dump()}

    raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Hotel not created, Back-end error.")


@hotels_router.delete("/{room_id}", summary="Delete hotel by id", response_model=HotelsResponseSchema)
async def delete_hotel_by_id(room_id: int, session: AsyncSession = Depends(get_db)) -> dict[str, Any] | None:
    deleted_hotel: Hotels | None = await HotelsRepo.delete_by_id(session=session, id_to_delete=room_id)

    if deleted_hotel:
        response_obj = HotelsResponseSchema(
            id=deleted_hotel.id,
            name=deleted_hotel.name,
            country=deleted_hotel.country,
            city=deleted_hotel.city,
            rating=deleted_hotel.rating
        )

        return {**response_obj.model_dump()}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with id {room_id} was not found")
