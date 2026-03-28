from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import Users
from app.repo.base_repo import BaseRepo


class UsersRepo(BaseRepo[Users]):
    model = Users

    @staticmethod
    async def find_by_id(id_to_find: int, session: AsyncSession) -> Users | None:
        query = select(Users).where(Users.id == id_to_find)

        result = await session.execute(query)
        found_obj = result.scalar()

        return found_obj

    @staticmethod
    async def find_by_contact_info(session: AsyncSession, email: str | None = None, phone_number: str | None = None) -> Users | None:
        query = select(Users)

        if email:
            query = query.where(Users.email == email)

        else:
            query = query.where(Users.phone_number == phone_number)

        result = await session.execute(query)
        user = result.scalar()

        return user
