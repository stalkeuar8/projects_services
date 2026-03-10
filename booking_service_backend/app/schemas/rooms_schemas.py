from pydantic import BaseModel, Field, TypeAdapter
from enum import Enum
from typing import List, Annotated

CapacityValid = Annotated[int, Field(ge=1, le=3)]
PriceValid = Annotated[int, Field(ge=0)]


class RoomCategory(str, Enum):
    standart = 'standart'
    superior = 'superior'
    lux = 'lux'
    presidental = 'presidental'


class RoomsSchema(BaseModel):
    hotel_id: int
    category: RoomCategory
    capacity: CapacityValid
    price_per_night: PriceValid


rooms_adapter = TypeAdapter(List[RoomsSchema])
