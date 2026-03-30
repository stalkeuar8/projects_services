import bcrypt

from typing import Self
from pydantic import BaseModel, model_validator

class HotelPasswordSchema(BaseModel):
    password: str
    hashed_password: bytes | None = None

    @model_validator(mode='after')
    def hash_password(self) -> Self:
        self.hashed_password = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt())

        return self

class HotelLoginSchema(BaseModel):
    hotel_id: int
    chat_id: str