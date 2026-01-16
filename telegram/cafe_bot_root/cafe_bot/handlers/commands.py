from aiogram import types, Router, F
from aiogram.filters import Command

router = Router()

@router.message(Command('help'))
async def show_help(message: types.Message):
    await message.answer('Available commands:\n\n/start - Start bot\n/menu - See menu\n'
                         '/show_cart - Show your cart\n/clear_cart - Clear your cart\n\n'
                         'Use "/" to write a command!')


