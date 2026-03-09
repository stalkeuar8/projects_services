from app.models.booking import Clients
from app.orms.base_orm import BaseOrm
from app.settings.database import async_session_factory
from app.utils.transaction_deco import transaction
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession 
import asyncio



class ClientsOrm(BaseOrm):

    @transaction
    @staticmethod
    async def create(session: AsyncSession, incoming_data: dict):
        new_client = Clients(**incoming_data)
        session.add(new_client)


    @transaction
    @staticmethod
    async def multi_create(session: AsyncSession, incoming_data_list: list[dict]):
        clients = [
            Clients(**client) for client in incoming_data_list
        ]

        session.add_all(clients)


    @transaction
    @staticmethod
    async def find_by_id(session: AsyncSession, id_to_find: int):
        query = (
            select(Clients)
            .filter_by(id=id_to_find)
        )
        client = await session.execute(query).scalar_one_or_none()
        return client


    @transaction
    @staticmethod
    async def multi_find_by_ids(session: AsyncSession, id_to_find_list: list[int]):
        query = (
            select(Clients)
            .where(Clients.id.in_(id_to_find_list))
        )
        clients = await session.execute(query).scalars().all()
        return clients


    @transaction
    @staticmethod
    async def find_by_name(session: AsyncSession, name_element: str):
        query = (
            select(Clients)
            .where(Clients.full_name.like(name_element))
        )
        client = await session.execute(query).scalar_one_or_none()
        return client


    @transaction
    @staticmethod
    async def find_by_phone_number(session: AsyncSession, phone_number: str):
        query = (
            select(Clients)
            .filter_by(phone_number=phone_number)
        )
        client = await session.execute(query).scalar_one_or_none()
        return client


    @transaction
    @staticmethod
    async def delete_by_id(session: AsyncSession, id_to_delete: int):
        query = (
            delete(Clients)
            .where(Clients.id == id_to_delete)\
            .returning(Clients)
        )
        client = await session.execute(query)
        client_to_delete = client.scalar_one_or_none()

        if not client_to_delete:
            raise ValueError("Client was not found")
            
        return client_to_delete
