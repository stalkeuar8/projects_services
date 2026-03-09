from app.orms.base_orm import create_tables
from app.orms.bookings_orm import BookingsOrm
from app.orms.hotels_orm import HotelsOrm
import asyncio

async def main():

    await create_tables()


if __name__ == '__main__':
    asyncio.run(main())