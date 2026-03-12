from pydantic import BaseModel, Field
from typing import Annotated

RatingValid = Annotated[int, Field(ge=1, le=5)]


class HotelsSchema(BaseModel):
    name: str
    country: str
    city: str
    rating: RatingValid
