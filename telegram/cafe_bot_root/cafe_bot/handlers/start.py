from aiogram import types, Router, F
from aiogram.filters import Command
from cafe_bot.keyboards.menu import generate_menu_kb
from cafe_bot.database.filling_getting_user_info import extract_exact_user_info, register_user_to_db
from cafe_bot.logs.logging import logger

router = Router()
path = r'D:\coding\python\telegram\cafe_bot\general_info.json'

@router.message(Command('start'))
async def start_bot(message: types.Message):
    if extract_exact_user_info(str(message.from_user.id)):
        logger.bind(type='system').info(
            f"User {message.from_user.username} ({message.from_user.id}) started bot as OLD user!")
    else:
        logger.bind(type='system').info(
            f"User {message.from_user.username} ({message.from_user.id}) started bot as NEW user!")
        register_user_to_db(str(message.from_user.id), message.from_user.username, message.from_user.first_name)

    await message.answer("Welcome!\n\nIt is Cafe bot! Here you can order any of desired drink or "
                         "dessert! Look throw our menu to make a choice!\n\nUse /help to see more info!",
                         reply_markup=generate_menu_kb())


