from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Self

from pydantic import BaseModel, Field, field_validator, model_validator


class BookingStatus(str, Enum):
    booked = "booked"
    pending = "pending"
    checked_in = "checked in"
    completed = "completed"
    canceled = "canceled"


class BookingsBaseSchema(BaseModel):
    room_id: int
    check_in: datetime
    check_out: datetime

    @field_validator("check_in")
    @classmethod
    def validate_date(cls, date: datetime) -> datetime:
        if date <= datetime.now(tz=timezone.utc):
            raise ValueError("BookingsSchema ERROR: Value 'check_in' must be later than now!")
        return date

    @model_validator(mode="after")
    def validate_check_out(self) -> Self:
        if self.check_out < self.check_in + timedelta(days=1):
            raise ValueError("BookingsSchema ERROR: Value 'check_out' must be later than check in plus 1 day!")
        return self


class BookingsPreparationSchema(BookingsBaseSchema):
    pass


class BookingsCreateSchema(BookingsBaseSchema):
    user_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_price: int = Field(ge=0)
    status: BookingStatus


class BookingsResponseSchema(BookingsBaseSchema):
    id: int
    user_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    total_price: int = Field(ge=0)




class AvailabilityForBookingResponseSchema(BookingsBaseSchema):
    is_available: bool


class AvailabilityForBookingRequestSchema(BookingsBaseSchema):
    pass


class ChangeBookingStatusSchema(BaseModel):
    id: int
    status: BookingStatus


class BookingsStatsRequestSchema(BaseModel):
    created_after: datetime | None = None
    created_before: datetime | None = None
    room_id: int | None = None
    hotel_id: int | None

    @classmethod
    @field_validator("created_after", "created_before", mode="after")
    def validate_timezone(cls, value: datetime) -> datetime:
        if value:
            if value.tzinfo is None:
                return value.replace(tzinfo=timezone.utc)

            return value.astimezone(timezone.utc)

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        if self.created_after and self.created_before:
            if self.created_after >= self.created_before:
                raise ValueError("Created after must be less than created before!")

        if self.created_before or self.created_after:
            if self.created_after >= datetime.now(tz=timezone.utc) or self.created_before >= datetime.now(tz=timezone.utc):
                raise ValueError("Created after AND created before must be less than now!")


class BookingStatsResponseSchema(BaseModel):
    total_bookings: int
    total_completed_bookings: int
    total_canceled_bookings: int
    total_checked_in_bookings: int
    total_booked_bookings: int
    total_pending_bookings: int
