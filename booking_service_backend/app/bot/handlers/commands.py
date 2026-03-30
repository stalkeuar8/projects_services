from aiogram import F, Router, types
from aiogram.filters import Command

commands_router = Router()


@commands_router.message(Command("start"))
async def start_response(message: types.Message):
    await message.answer(text="hello")
