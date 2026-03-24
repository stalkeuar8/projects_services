from enum import Enum
from typing import Annotated, Self

from pydantic import BaseModel, Field, model_validator

from app.models.hotel import Rooms

CapacityValid = Annotated[int, Field(ge=1, le=3)]
PriceValid = Annotated[int, Field(ge=0)]


class RoomCategory(str, Enum):
    standart = "standart"
    superior = "superior"
    lux = "lux"
    presidental = "presidental"


class RoomsSchema(BaseModel):
    hotel_id: int
    category: RoomCategory
    capacity: CapacityValid
    price_per_night: PriceValid


class RoomsResponseSchema(BaseModel):
    id: int
    hotel_id: int
    category: RoomCategory
    capacity: CapacityValid
    price_per_night: PriceValid



class RoomsListResponse(BaseModel):

    rooms: list[RoomsResponseSchema]
    total: int | None

    @model_validator(mode='after')
    def calculate_total(self) -> Self:
        rooms_length = len(self.rooms)

        if not self.total or self.total != rooms_length:
            self.total = rooms_length

        return self
    

class RoomsCreateSchema(BaseModel):
    hotel_id: int
    category: RoomCategory
    capacity: CapacityValid
    price_per_night: PriceValid