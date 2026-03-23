from fastapi import Depends, APIRouter, Query

from sqlalchemy.ext.asyncio import AsyncSession

from typing import Sequence, Annotated

from app.settings.database import get_db
from app.schemas.rooms_schemas import RoomsResponseSchema
from app.utils.room_search_filter import RoomSearchFilters
from app.models.hotel import Rooms
from app.orms.rooms_orm import RoomsOrm


rooms_router = APIRouter(prefix="/rooms", tags=['Rooms'])


@rooms_router.get(summary='Get rooms by filters', response_model=Sequence[RoomsResponseSchema])
async def get_hotels_by_filters(filters: Annotated[RoomSearchFilters, Query()], session: AsyncSession = Depends(get_db)) -> Sequence[Rooms] | None:
    rooms: Sequence[Rooms] | None = await RoomsOrm.find_room_by_filters(filters=filters, session=session)

    if rooms:
        return {"status code":200, "results":rooms}
    
    return {"status code":200, "results":[]}