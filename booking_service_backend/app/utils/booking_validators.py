from pydantic import BaseModel, Field, TypeAdapter
from enum import Enum
import datetime

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
