from typing import Annotated, Any, Sequence

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Clients
from app.repo.clients_repo import ClientsRepo
from app.schemas.clients_schemas import ClientsCreateSchema, ClientsListResponseSchema, ClientsResponseSchema
from app.settings.database import get_db

clients_router = APIRouter(prefix="/clients", tags=["Clients"])


@clients_router.get("/{client_id}", summary="Get all clients", response_model=ClientsResponseSchema)
async def get_client_by_id(client_id: int, session: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    client: Clients | None = await ClientsRepo.find_by_id(session=session, id_to_find=client_id)

    if client:
        response_obj = ClientsResponseSchema(id=client.id, full_name=client.full_name, phone_number=client.phone_number, email=client.email)

        return {**response_obj.model_dump()}

    raise HTTPException(status_code=404, detail=f"Client with id {client_id} was not found")


@clients_router.post("/", summary="Create client", response_model=ClientsResponseSchema)
async def create_client(body: ClientsCreateSchema, session: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    new_client: Clients | None = await ClientsRepo.create(session=session, inserting_data_dto=body)

    if new_client:
        response_obj = ClientsResponseSchema(id=new_client.id, full_name=new_client.full_name, phone_number=new_client.phone_number, email=new_client.email)

        return {**response_obj.model_dump()}

    raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Client not created, Back-end error.")


@clients_router.delete("/{client_id}", summary="Delete client by id", response_model=ClientsResponseSchema)
async def delete_client(client_id: int, session: AsyncSession = Depends(get_db)) -> dict[str, Any]:
    deleted_client: Clients | None = await ClientsRepo.delete_by_id(id_to_delete=client_id, session=session)

    if deleted_client:
        response_obj = ClientsResponseSchema(id=deleted_client.id, full_name=deleted_client.full_name, phone_number=deleted_client.phone_number, email=deleted_client.email)

        return {**response_obj.model_dump()}

    raise HTTPException(status_code=404, detail=f"Client with id {client_id} was not found")



