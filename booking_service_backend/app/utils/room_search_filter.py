from pydantic import BaseModel
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
