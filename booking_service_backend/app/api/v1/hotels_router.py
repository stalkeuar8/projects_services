from typing import Annotated, Any, Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.response_parser import create_hotel_response
from app.models.hotel import Hotels
from app.repo.hotels_repo import HotelsRepo
from app.schemas.hotels_schemas import HotelsCreateSchema, HotelSearchFilters, HotelsListResponseSchema, HotelsResponseSchema
from app.settings.database import get_db

hotels_router = APIRouter(prefix="/hotels", tags=["Hotels"])


@hotels_router.get("/", summary="Get hotels by filters", response_model=HotelsListResponseSchema)
async def get_hotels_by_filters(body: Annotated[HotelSearchFilters, Query()], session: AsyncSession = Depends(get_db)) -> HotelsListResponseSchema:
    hotels: Sequence[Hotels] | None = await HotelsRepo.find_hotel_by_filters(filters=body, session=session)

    if hotels:
        return HotelsListResponseSchema(hotels=hotels)

    return HotelsListResponseSchema(hotels=[], total=0)


@hotels_router.get("/{hotel_id}", summary="Get hotel by id", response_model=HotelsResponseSchema)
async def get_hotel_by_id(hotel_id: int, session: AsyncSession = Depends(get_db)) -> HotelsResponseSchema | None:
    hotel: Hotels | None = await HotelsRepo.find_by_id(id_to_find=hotel_id, session=session)

    if hotel:
        return create_hotel_response(hotel_obj=hotel)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hotel with id {hotel_id} was not found")

