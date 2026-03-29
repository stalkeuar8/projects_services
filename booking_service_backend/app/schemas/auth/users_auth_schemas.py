from enum import Enum

import bcrypt
from pydantic import BaseModel, EmailStr, model_validator

from app.schemas.users_schemas import UserBaseSchema


class UsersRole(str, Enum):
    CLIENT = "client"
    ADMIN = "admin"


class UserLoginRequestSchema(BaseModel):
    password: str
    email: EmailStr | None = None
    phone_number: str | None = None


class UserRegisterRequestSchema(UserBaseSchema):
    password: str
    hashed_password: bytes = None

    @model_validator(mode="after")
    def hash_password(self):
        self.hashed_password = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt())
        return self


class UserAuthResponseSchema(UserBaseSchema):
    id: int
    role: UsersRole
    is_logined: bool
    jwt_token: str
