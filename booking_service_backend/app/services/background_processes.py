from app.models.booking import Bookings
from sqlalchemy import select, delete
from app.settings.database import async_session_factory
import asyncio


class BackgroundCleaner:

    @staticmethod
    async def background_bookings_cleaner(time_frequency_mins: int = 5):
        while True:
            try: 
                async with async_session_factory.begin() as session:
                        query = (
                            delete(Bookings)
                            .where(Bookings.status=='pending')
                        )

                        await session.execute(query)

            except Exception as e:  
                print(f"Background bookings cleaner ERROR: {e}")

            await asyncio.sleep(time_frequency_mins*60)    


