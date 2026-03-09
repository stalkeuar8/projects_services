from app.models.booking import Clients
from app.orms.base_orm import BaseOrm
from app.settings.database import async_session_factory
from sqlalchemy import select
import asyncio



class ClientsOrm(BaseOrm):

    @staticmethod
    async def create(incoming_data: dict):
        async with async_session_factory() as session:
            new_client = Clients(**incoming_data)
            session.add(new_client)
            await session.commit()


    @staticmethod
    async def multi_create(incoming_data_list: list[dict]):
        async with async_session_factory() as session:
            clients = [
                Clients(**client) for client in incoming_data_list
            ]

            session.add_all(clients)
            await session.commit()


    @staticmethod
    async def find_by_id(id_to_find: int):
        pass


    @staticmethod
    async def multi_find_by_ids(id_to_find_list: list[int]):
        pass


    @staticmethod
    async def find_by_name(name_element: str):
        pass


    @staticmethod
    async def find_by_phone_number(phone_number: str):
        pass


    @staticmethod
    async def delete_by_id(id_to_delete: int):
        pass

