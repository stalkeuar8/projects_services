from app.models.booking import Bookings
from sqlalchemy import delete, update
from app.settings.database import async_session_factory
import asyncio
import datetime


class BackgroundProcesses:

    @staticmethod
    async def background_bookings_cleaner(time_frequency_mins: int = 5):
        while True:
            try:
                async with async_session_factory.begin() as session:
                    query = delete(Bookings).where(Bookings.status == "pending")

                    await session.execute(query)

            except Exception as e:
                print(f"Background bookings cleaner ERROR: {e}")

            await asyncio.sleep(time_frequency_mins * 60)

    @staticmethod
    async def background_status_checker():
        while True:
            try:
                async with async_session_factory.begin() as session:
                    query = (
                        update(Bookings)
                        .values(status="completed")
                        .where(Bookings.check_out < datetime.datetime.now())
                    )

                    await session.execute(query)

            except Exception as e:
                print(f"Background status checker ERROR: {e}")

            await asyncio.sleep(86400)
