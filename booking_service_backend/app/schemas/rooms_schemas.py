from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.models.hotel import Rooms
from app.schemas.hotels_schemas import RatingValid

CapacityValid = Annotated[int, Field(ge=1, le=3)]
PriceValid = Annotated[int, Field(ge=0)]


class RoomCategory(str, Enum):
    standart = "standart"
    superior = "superior"
    lux = "lux"
    presidental = "presidental"


class RoomBaseSchema(BaseModel):
    hotel_id: int
    category: RoomCategory
    capacity: CapacityValid
    price_per_night: PriceValid

class RoomsSchema(RoomBaseSchema):
    pass

class RoomsCreateSchema(RoomBaseSchema):
    pass


class RoomsResponseSchema(RoomBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    
    id: int


class RoomsListResponseSchema(BaseModel):
    rooms: list[RoomsResponseSchema]
    total: int | None

    @model_validator(mode="after")
    def calculate_total(self) -> Self:
        rooms_length = len(self.rooms)

        if not self.total or self.total != rooms_length:
            self.total = rooms_length

        return self



class RoomSearchFilters(BaseModel):
    country: str | None = None

    city: str | None = None

    min_rating: RatingValid | None = None
    max_rating: RatingValid | None = None

    category: RoomCategory | None = None

    min_capacity: CapacityValid | None = None
    max_capacity: CapacityValid | None = None

    min_price: PriceValid | None = None
    max_price: PriceValid | None = None

    check_in: datetime | None = None
    check_out: datetime | None = None

    @field_validator("check_in")
    def validate_date(cls, date: datetime) -> datetime:
        if date <= datetime.now(tz=timezone.utc):
            raise ValueError("RoomSearchFilters ERROR: Value 'check_in' must be later than now!")
        return date

    @model_validator(mode="after")
    def validate_check_out(self) -> Self:
        if self.min_rating and self.max_rating and self.min_rating >= self.max_rating:
            raise ValueError("RoomSearchFilters ERROR: Value 'min_rating' must be less than 'max_rating'!")

        if self.min_capacity and self.max_capacity and self.min_capacity >= self.max_capacity:
            raise ValueError("RoomSearchFilters ERROR: Value 'min_capacity' must be less than 'max_capacity'!")

        if self.min_price and self.max_price and self.min_price >= self.max_price:
            raise ValueError("RoomSearchFilters ERROR: Value 'min_price' must be less than 'max_price'!")

        if self.check_out < self.check_in + timedelta(days=1):
            raise ValueError("RoomSearchFilters ERROR: Value 'check_out' must be later than check in plus 1 day!")
        return self


