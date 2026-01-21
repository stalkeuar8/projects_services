import os

from aiogram import Bot, Dispatcher
import asyncio
from cafe_bot.handlers.__init__ import route_generator
from cafe_bot.logs.logging import logger
from cafe_bot.config import BOT_TOKEN

async def main():
    try:
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()
        route_generator(dp)
        logger.bind(type='system').info("Bot started!")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"ERROR: {e}")

try:
    if __name__ == "__main__":
        asyncio.run(main())

except Exception as e:
    logger.error(f"ERROR: {e}")

