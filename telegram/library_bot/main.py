from aiogram import Bot, Dispatcher, Router, types
import asyncio
from handlers.__init__ import register_routes
from handlers.start import start_bot
from database.models import BaseModel
from database import engine

TOKEN = '8541388465:AAGQYI8j_Sv8Btim38mP1XS_SM1RRegGVbo'

async def init_model():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    register_routes(dp)
    await init_model()
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        print("\nBot stopped!\n")