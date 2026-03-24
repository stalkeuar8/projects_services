from app.models.booking import Clients
from app.orms.base_orm import BaseOrm

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class ClientsOrm(BaseOrm[Clients]):
    model = Clients

    @staticmethod
    async def find_by_id(id_to_find: int, session: AsyncSession) -> Clients | None:
        query = (
            select(Clients)
            .where(Clients.id==id_to_find)
        )

        result = await session.execute(query)
        found_obj = result.scalar()

        return found_obj