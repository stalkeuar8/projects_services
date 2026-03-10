from pydantic import BaseModel, Field, TypeAdapter
from enum import Enum
from typing import List, Annotated


RatingValid = Annotated[int, Field(ge=1, le=5)]

class HotelsSchema(BaseModel):
    name: str
    country: str
    city: str
    rating: RatingValid 


hotels_adapter = TypeAdapter(List[HotelsSchema])