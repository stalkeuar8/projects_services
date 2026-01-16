from aiogram import Router, types
from aiogram.filters import Command
from telegram.library_bot.keyboards.menu import main_menu_kb

router = Router()

@router.message(Command("start"))
async def start_bot(message: types.Message):
    await message.answer(f"Hello, {message.from_user.first_name}! I am Library!", reply_markup=main_menu_kb())