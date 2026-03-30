from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Bookings
from app.models.user import Users
from app.repo.base_admin_repo import BaseAdminRepo
from app.repo.base_repo import BaseRepo
from app.schemas.users_schemas import UserStatsResponseSchema


class UsersRepo(BaseRepo[Users]):
    model = Users

    @staticmethod
    async def get_my_bookings(current_user_id: int, session: AsyncSession) -> Bookings | None:
        query = select(Bookings).where(Bookings.user_id == current_user_id)

        results = await session.execute(query)
        bookings = results.scalars().all()

        return bookings


class AdminUsersRepo(BaseAdminRepo[Users]):
    model = Users

    @staticmethod
    async def admin_find_by_contact_info(session: AsyncSession, email: str | None = None, phone_number: str | None = None) -> Users | None:
        query = select(Users).where(Users.deleted_at == None)

        if email:
            query = query.where(Users.email == email)

        else:
            query = query.where(Users.phone_number == phone_number)

        result = await session.execute(query)
        user = result.scalar()

        return user

    @staticmethod
    async def admin_get_users_stats(user_id: int, session: AsyncSession) -> UserStatsResponseSchema | None:

        query = select(Bookings).where(Bookings.user_id == user_id)

        results = await session.execute(query)
        bookings = results.scalars().all()

        if bookings:
            return UserStatsResponseSchema(
                users_bookings=bookings,
                total_orders_price=sum([booking.total_price for booking in bookings]),
                total_bookings=len(bookings),
                total_booked_bookings=len([booking for booking in bookings if booking.status == "booked"]),
                total_canceled_bookings=len([booking for booking in bookings if booking.status == "canceled"]),
                total_completed_bookings=len([booking for booking in bookings if booking.status == "completed"]),
                total_checked_in_bookings=len([booking for booking in bookings if booking.status == "checked_in"]),
                total_pending_bookings=len([booking for booking in bookings if booking.status == "pending"]),
            )

        return None
