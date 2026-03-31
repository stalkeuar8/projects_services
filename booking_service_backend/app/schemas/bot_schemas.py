from pydantic import BaseModel

from app.schemas.bookings_schemas import BookingsResponseSchema


class BookingApproveRequestSchema(BaseModel):
    booking_info: BookingsResponseSchema
    hotel_id: int


class BookingApproveProcessSchema(BookingApproveRequestSchema):
    pass


class BookingApproveResponseSchema(BaseModel):
    approving_result: bool
    booking_id: int
