from pydantic import BaseModel, model_validator
from app.schemas.hotels_schemas import RatingValid
from app.schemas.rooms_schemas import RoomCategory, CapacityValid, PriceValid


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


    @model_validator(mode="after")
    def validate_check_out(self):
        if self.min_rating and self.max_rating and self.min_rating >= self.max_rating:
            raise ValueError(
                "RoomSearchFilters ERROR: Value 'min_rating' must be less than 'max_rating'!"
            )
        
        if self.min_capacity and self.max_capacity and self.min_capacity >= self.max_capacity:
            raise ValueError(
                "RoomSearchFilters ERROR: Value 'min_capacity' must be less than 'max_capacity'!"
            )
        
        if self.min_price and self.max_price and self.min_price >= self.max_price:
            raise ValueError(
                "RoomSearchFilters ERROR: Value 'min_price' must be less than 'max_price'!"
            )
        
        return self