from typing import Self

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from app.schemas.bookings_schemas import BookingsResponseSchema


class UserBaseSchema(BaseModel):
    full_name: str
    phone_number: str
    email: EmailStr


class UsersCreateSchema(UserBaseSchema):
    hashed_password: bytes


class UsersResponseSchema(UserBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UsersListResponseSchema(BaseModel):
    users: list[UsersResponseSchema]
    total: int | None = None

    @model_validator(mode="after")
    def calculate_total(self) -> Self:
        users_length = len(self.users)

        if not self.total or self.total != users_length:
            self.total = users_length

        return self


class UserStatsResponseSchema(BaseModel):
    users_bookings: list[BookingsResponseSchema]
    total_orders_price: int = Field(ge=0)
    total_bookings: int = Field(ge=0)
    total_completed_bookings: int = Field(ge=0)
    total_canceled_bookings: int = Field(ge=0)
    total_checked_in_bookings: int = Field(ge=0)
    total_booked_bookings: int = Field(ge=0)
    total_pending_bookings: int = Field(ge=0)
