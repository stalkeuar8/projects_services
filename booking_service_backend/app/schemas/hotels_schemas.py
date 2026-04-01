from typing import Annotated, Self, Sequence

from pydantic import BaseModel, Field, model_validator

RatingValid = Annotated[int, Field(ge=1, le=5)]


class HotelsSchema(BaseModel):
    name: str
    country: str
    city: str
    rating: RatingValid


class HotelsResponseSchema(BaseModel):
    id: int
    name: str
    country: str
    city: str
    rating: RatingValid


class HotelsCreateSchema(BaseModel):
    name: str
    country: str
    city: str
    rating: RatingValid


class HotelsCreateListSchema(BaseModel):
    hotels_list: Sequence[HotelsCreateSchema]


class HotelsCreateListResponseSchema(BaseModel):
    hotels_list: Sequence[HotelsResponseSchema]


class HotelsListResponseSchema(BaseModel):
    hotels: Sequence[HotelsResponseSchema]
    total: int | None

    @model_validator(mode="after")
    def calculate_total(self) -> Self:
        hotels_length = len(self.hotels)

        if not self.total or self.total != hotels_length:
            self.total = hotels_length

        return self


class HotelSearchFilters(BaseModel):
    country: str | None = None
    city: str | None = None
    min_rating: RatingValid | None = None
    max_rating: RatingValid | None = None


class HotelEditSchema(BaseModel):
    name: str | None = None
    country: str | None = None
    city: str | None = None
    rating: RatingValid | None = None
