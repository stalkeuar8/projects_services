from typing import Self

from pydantic import BaseModel, model_validator


class ClientsCreateSchema(BaseModel):
    full_name: str
    phone_number: str


class ClientsResponseSchema(BaseModel):
    id: int
    full_name: str
    phone_number: str


class ClientsListResponseSchema(BaseModel):
    clients: list[ClientsResponseSchema]
    total: int | None = None

    @model_validator(mode="after")
    def calculate_total(self) -> Self:
        clients_length = len(self.clients)

        if not self.total or self.total != clients_length:
            self.total = clients_length

        return self
