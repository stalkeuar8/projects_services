from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum
import datetime


class BookingStatus(str, Enum):
    booked = "booked"
    pending = "pending"
    completed = "completed"
    canceled = "canceled"


class BookingsCheckAvailableSchema(BaseModel):
    room_id: int
    check_in: datetime.datetime
    check_out: datetime.datetime


class BookingsSchema(BaseModel):
    room_id: int
    client_id: int
    check_in: datetime.datetime
    check_out: datetime.datetime
    total_price: int = Field(ge=0)
    status: BookingStatus

    @field_validator("check_in")
    @classmethod
    def validate_date(cls, date: datetime.datetime):
        if date <= datetime.datetime.now():
            raise ValueError(
                "BookingsSchema ERROR: Value 'check_in' must be later than now!"
            )
        return date

    @model_validator(mode="after")
    def validate_check_out(self):
        if self.check_out < self.check_in + datetime.timedelta(days=1):
            raise ValueError(
                "BookingsSchema ERROR: Value 'check_out' must be later than check in plus 1 day!"
            )
        return self
