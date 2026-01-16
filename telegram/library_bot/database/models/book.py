from telegram.library_bot.database.models.__init__ import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey

class Book(BaseModel):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int] # 1$ = 100 cents
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))