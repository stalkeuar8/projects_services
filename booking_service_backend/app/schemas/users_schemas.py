from typing import Self

from pydantic import BaseModel, EmailStr, model_validator


class UserBaseSchema(BaseModel):
    full_name: str
    phone_number: str
    email: EmailStr


class UsersCreateSchema(UserBaseSchema):
    hashed_password: bytes


class UsersResponseSchema(UserBaseSchema):
    id: int


class DeletedUserResponseSchema(UsersResponseSchema):
    is_deleted: bool


class UsersListResponseSchema(BaseModel):
    users: list[UsersResponseSchema]
    total: int | None = None

    @model_validator(mode="after")
    def calculate_total(self) -> Self:
        users_length = len(self.users)

        if not self.total or self.total != users_length:
            self.total = users_length

        return self
