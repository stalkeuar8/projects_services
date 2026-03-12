from app.models.booking import Clients
from app.orms.base_orm import BaseOrm
from app.schemas.clients_schemas import ClientsSchema
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession 


class ClientsOrm(BaseOrm):

    @staticmethod
    async def create(incoming_data_dto: ClientsSchema, session: AsyncSession):
        new_client = Clients(**incoming_data_dto.model_dump())
        session.add(new_client)


    @staticmethod
    async def multi_create(incoming_data_list_dto: list[ClientsSchema], session: AsyncSession):
        clients = [
            Clients(**client.model_dump()) for client in incoming_data_list_dto
        ]

        session.add_all(clients)


    @staticmethod
    async def find_by_id(id_to_find: int, session: AsyncSession) -> Clients:
        query = (
            select(Clients)
            .where(Clients.id==id_to_find)
        )
        result = await session.execute(query)
        client = result.scalar_one_or_none()
        return client


    @staticmethod
    async def multi_find_by_ids(id_to_find_list: list[int], session: AsyncSession):
        query = (
            select(Clients)
            .where(Clients.id.in_(id_to_find_list))
        )
        results = await session.execute(query)
        clients = results.scalars().all()
        return clients


    @staticmethod
    async def find_by_name(name_element: str, session: AsyncSession):
        query = (
            select(Clients)
            .where(Clients.full_name.contains(name_element))
        )
        results = await session.execute(query)
        clients = results.scalars().all()
        return clients


    @staticmethod
    async def find_by_phone_number(phone_number: str, session: AsyncSession):
        query = (
            select(Clients)
            .filter_by(phone_number=phone_number)
        )
        res = await session.execute(query)
        client = res.scalar_one_or_none()
        return client


    @staticmethod
    async def delete_by_id(id_to_delete: int, session: AsyncSession):
        query = (
            delete(Clients)
            .where(Clients.id == id_to_delete)
            .returning(Clients)
        )
        client = await session.execute(query)
        client_to_delete = client.scalar_one_or_none()

        if not client_to_delete:
            raise ValueError("Client was not found")
            
        return client_to_delete

    