from typing import Annotated, Sequence, Any

from fastapi import APIRouter, Depends, Query, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Clients
from app.orms.clients_orm import ClientsOrm
from app.schemas.clients_schemas import ClientsCreateSchema, ClientsResponseSchema, ClientsListResponseSchema
from app.settings.database import get_db


clients_router = APIRouter(prefix="/clients", tags=['Clients'])


@clients_router.get("/{client_id}", summary="Get all clients", response_model=ClientsResponseSchema)
async def get_client_by_id(client_id: int, session: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    client: Clients | None = await ClientsOrm.find_by_id(session=session, id_to_find=client_id)

    if client:
        return {
            **ClientsResponseSchema(
                id=client.id,
                full_name=client.full_name,
                phone_number=client.phone_number
            ).model_dump()
        }
    
    raise HTTPException(status_code=404, detail=f"Client with id {client_id} was not found")


@clients_router.post("/", summary="Create client", response_model=ClientsResponseSchema)
async def create_client(body: ClientsCreateSchema, session: AsyncSession = Depends(get_db)) -> Clients:
    return await ClientsOrm.create(session=session, inserting_data_dto=body)


@clients_router.delete("/{client_id}", summary="Delete client by id", response_model=ClientsResponseSchema)
async def delete_client(client_id: int, session: AsyncSession = Depends(get_db)) -> Clients:
    deleted_client: Clients | None = await ClientsOrm.delete_by_id(id_to_delete=client_id, session=session)

    if deleted_client: 
        return {
            **ClientsResponseSchema(
                id=deleted_client.id,
                full_name=deleted_client.full_name,
                phone_number=deleted_client.phone_number
            ).model_dump()
        }
    
    raise HTTPException(status_code=404, detail=f"Client with id {client_id} was not found")