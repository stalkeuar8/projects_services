import sqlite3
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from telegram.library_bot.database.models.category import Category
from telegram.library_bot.database.models.book import Book
from telegram.library_bot.database.models.user import User

engine = create_async_engine(
    url='sqlite+aiosqlite:///book_shop.db'
)
session_maker = async_sessionmaker(engine, expire_on_commit=False)

__all__ = [
    Category,
    User,
    Book
]