from app.utils.time_validator import FutureTimeValidator
from pydantic import BaseModel, Field
from enum import Enum
import datetime

class BookingCreateDTO(BaseModel):

    room_id: int
    check_in: datetime.datetime = FutureTimeValidator()
    check_out: datetime.datetime = FutureTimeValidator()


class BookingStatus(str, Enum):
    booked = 'booked'
    pending = 'pending'
    completed = 'completed'
    canceled = 'canceled'


class BookingsSchema(BaseModel):
    apart_id: int
    client_id: int
    check_in: datetime.datetime
    check_out: datetime.datetime
    total_price: int = Field(ge=0)
    status: BookingStatus