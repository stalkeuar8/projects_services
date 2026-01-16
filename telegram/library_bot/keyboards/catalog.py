from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

class CategoryCBdata(CallbackData, prefix="category"):
    category: str

class BookCBdata(CallbackData, prefix='book'):
    id: int
    category: str

def generate_catalog_kb(catalog):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for cat_cb, category in catalog.items():
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text=category['text'], callback_data=CategoryCBdata(category=cat_cb).pack())]
        )
    return keyboard

def generate_books_kb(books, category):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for book in books:
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text=book['name'], callback_data=BookCBdata(id=book['id'], category=category).pack())]
        )
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="Back to category", callback_data='catalog')]
    )
    return keyboard

def back_to_category_books(category):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Back to books", callback_data=CategoryCBdata(category=category).pack())]
        ]
    )