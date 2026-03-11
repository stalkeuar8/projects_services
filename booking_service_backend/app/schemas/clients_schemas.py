from pydantic import BaseModel

class ClientsSchema(BaseModel):

    id: int
    full_name: str
    phone_number: str