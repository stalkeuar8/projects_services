import datetime
from typing import Annotated

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column

id_primary_key = Annotated[int, mapped_column(primary_key=True)]
non_empty_str = Annotated[str, mapped_column(nullable=False)]
not_null_int = Annotated[int, mapped_column(nullable=False)]
datetime_utc_timezone = Annotated[datetime.datetime, mapped_column(DateTime(timezone=True), nullable=True)]


class Base(DeclarativeBase):
    pass
