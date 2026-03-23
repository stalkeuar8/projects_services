from typing import Annotated

from pydantic import BaseModel, Field

RatingValid = Annotated[int, Field(ge=1, le=5)]


class HotelsSchema(BaseModel):
    name: str
    country: str
    city: str
    rating: RatingValid


class HotelsResponseSchema(BaseModel):
    name: str
    country: str
    city: str
    rating: RatingValid