import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.bot.handlers.commands import commands_router
from app.settings.config import bot_settings


async def main():
    logging.basicConfig(level=logging.INFO)
    try:
        bot = Bot(token=bot_settings.TOKEN)
        dp = Dispatcher()
        dp.include_router(commands_router)
        await dp.start_polling(bot)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    asyncio.run(main())
