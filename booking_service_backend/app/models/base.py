from sqlalchemy import MetaData, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from typing import Annotated

id_primary_key = Annotated[int, mapped_column(primary_key=True)]
non_empty_str = Annotated[str, mapped_column(nullable=False)]
not_null_int = Annotated[int, mapped_column(nullable=False)]

class Base(DeclarativeBase):
    pass