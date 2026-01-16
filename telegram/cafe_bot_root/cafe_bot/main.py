from aiogram import Bot, Dispatcher, Router
import asyncio
from cafe_bot.handlers.__init__ import route_generator
from cafe_bot.secret_info import TOKEN
from cafe_bot.logs.logging import logger

async def main():
    try:
        bot = Bot(token=TOKEN)
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

