import asyncio
import datetime

from sqlalchemy import delete, update

from app.models.booking import Bookings
from app.settings.database import async_session_factory


class BackgroundProcesses:
    @staticmethod
    async def background_bookings_cleaner(time_frequency_mins: int = 15) -> None:
        while True:
            try:
                async with async_session_factory.begin() as session:
                    time_gap = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=15)
                    query = delete(Bookings).where(Bookings.status == "pending", Bookings.created_at < time_gap)

                    await session.execute(query)

            except Exception as e:
                print(f"Background bookings cleaner ERROR: {e}")

            await asyncio.sleep(time_frequency_mins * 60)

    @staticmethod
    async def background_status_checker() -> None:
        while True:
            try:
                async with async_session_factory.begin() as session:
                    current_time = datetime.datetime.now(tz=datetime.timezone.utc)

                    check_out_query = update(Bookings).values(status="completed").where(Bookings.check_out < current_time)
                    check_in_query = update(Bookings).values(status="checked in").where(Bookings.check_in < current_time)

                    await session.execute(check_out_query)
                    await session.execute(check_in_query)

            except Exception as e:
                print(f"Background status checker ERROR: {e}")

            await asyncio.sleep(86400)
