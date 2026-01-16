from aiogram import Dispatcher
from cafe_bot.handlers.start import router as start_router
from cafe_bot.handlers.commands import router as commands_router
from cafe_bot.keyboards.main_page_buttons import router as main_page_bts_router

def route_generator(dp: Dispatcher):
    dp.include_router(start_router)
    dp.include_router(commands_router)
    dp.include_router(main_page_bts_router)