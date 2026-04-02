from enum import Enum
from typing import Self

import bcrypt
from pydantic import BaseModel, EmailStr, model_validator

from app.schemas.users_schemas import UserBaseSchema
from app.utils.hash_pass import get_password_hash

class UsersRole(str, Enum):
    CLIENT = "client"
    ADMIN = "admin"


class UserLoginRequestSchema(BaseModel):
    password: str
    email: EmailStr | None = None
    phone_number: str | None = None


class UserRegisterRequestSchema(UserBaseSchema):
    password: str
    hashed_password: str | None = None

    @model_validator(mode="after")
    def hash_password(self) -> Self:
        self.hashed_password = get_password_hash(self.password)
        return self


class UserAuthResponseSchema(UserBaseSchema):
    id: int
    role: UsersRole
    is_logined: bool
    jwt_token: str


class UserLogoutResponseSchema(BaseModel):
    status: int
    is_logged_out: bool
    message: str | None = None


class RefreshTokenRequestSchema(BaseModel):
    refresh_token: str


class RefreshTokenResponseSchema(BaseModel):
    access_token: str
    type: str
