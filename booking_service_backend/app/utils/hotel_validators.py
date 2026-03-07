from pydantic import BaseModel, Field, TypeAdapter
from enum import Enum
from typing import List


class HotelsSchema(BaseModel):
    name: str
    country: str
    city: str
    rating: int = Field(ge=1, le=5)


class RoomCategory(str, Enum):
    standart = 'standart'
    superior = 'superior'
    lux = 'lux'
    presidental = 'presidental'


class RoomsSchema(BaseModel):
    hotel_id: int
    category: RoomCategory
    capacity: int = Field(ge=1, le=3)
    price_per_night: int = Field(ge=0)


rooms_adapter = TypeAdapter(List[RoomsSchema])
hotels_adapter = TypeAdapter(List[HotelsSchema])