from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def generate_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='Menu ☕')],
            [KeyboardButton(text='Cart 🛒'), KeyboardButton(text='Contacts 📞')]
        ], resize_keyboard=True
    )

