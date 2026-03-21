from pydantic import BaseModel


class ClientsSchema(BaseModel):
    full_name: str
    phone_number: str
