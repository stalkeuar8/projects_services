import datetime

from sqlalchemy import update

from app.models.booking import Bookings
from app.settings.database import celery_session_factory
from app.schemas.bookings_schemas import BookingStatus


class BackgroundProcesses:
    @staticmethod
    async def background_bookings_cleaner() -> None:
        try:
            async with celery_session_factory.begin() as session:
                time_gap = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=15)
                query = update(Bookings).where(Bookings.status == BookingStatus.pending, Bookings.created_at < time_gap).values(status=BookingStatus.canceled)

                await session.execute(query)

        except Exception as e:
            print(f"Background bookings cleaner ERROR: {e}")

    @staticmethod
    async def background_status_checker() -> None:
        try:
            async with celery_session_factory.begin() as session:
                current_time = datetime.datetime.now(tz=datetime.timezone.utc)

                check_out_query = update(Bookings).values(status="completed").where(Bookings.check_out < current_time)
                check_in_query = update(Bookings).values(status="checked in").where(Bookings.check_in < current_time)

                await session.execute(check_out_query)
                await session.execute(check_in_query)

        except Exception as e:
            print(f"Background status checker ERROR: {e}")
