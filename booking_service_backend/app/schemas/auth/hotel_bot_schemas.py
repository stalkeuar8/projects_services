from typing import Self

import bcrypt
from pydantic import BaseModel, model_validator
from app.utils.hash_pass import get_password_hash

class HotelPasswordSchema(BaseModel):
    password: str
    hashed_password: str | None = None

    @model_validator(mode="after")
    def hash_password(self) -> Self:
        self.hashed_password = get_password_hash(self.password)

        return self


class HotelLoginSchema(BaseModel):
    hotel_id: int
    chat_id: str
