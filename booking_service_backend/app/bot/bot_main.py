from aiogram import Bot, Dispatcher
import asyncio
from app.settings.config import bot_settings

BOT_TOKEN = bot_settings.BOT_TOKEN

async def main():
    try:
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()
        await dp.start_polling(bot)
    except Exception as e:
        pass

try:
    if __name__ == "__main__":
        asyncio.run(main())

except Exception as e:
    pass