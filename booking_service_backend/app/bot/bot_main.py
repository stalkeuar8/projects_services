import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from app.bot.handlers.commands import commands_router
from app.bot.handlers.auth import auth_router
from app.settings.config import bot_settings
from app.bot.handlers.http_requests_handler import handle_external_request

from aiohttp import web

async def start_http_server(bot: Bot) -> None:
    bot_app = web.Application()
    bot_app['bot'] = bot

    bot_app.router.add_post(bot_settings.EXT_REQ_PATH, handle_external_request)

    runner = web.AppRunner(bot_app)
    await runner.setup()

    site = web.TCPSite(runner=runner, host=bot_settings.HOST, port=bot_settings.PORT)

    await site.start()

async def main():
    logging.basicConfig(level=logging.INFO)
    try:
        bot = Bot(token=bot_settings.TOKEN)
        dp = Dispatcher()
        dp.include_router(commands_router)
        dp.include_router(auth_router)

        asyncio.create_task(start_http_server(bot))

        await dp.start_polling(bot)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    try:
        asyncio.run(main())
        
    except Exception as e:
        print(f"BOT STOPPED, ERROR: {e}")