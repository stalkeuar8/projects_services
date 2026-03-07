from sqlalchemy import MetaData, ForeignKey, text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated
from app.models.base import Base, id_primary_key, non_empty_str, not_null_int
import datetime


class Clients(Base):
    __tablename__ = 'clients'

    id: Mapped[id_primary_key]
    full_name: Mapped[non_empty_str]
    phone_number: Mapped[non_empty_str] = mapped_column(unique=True)


class Bookings(Base):
    __tablename__ = 'bookings'

    id: Mapped[id_primary_key]
    apart_id: Mapped[not_null_int] = mapped_column(ForeignKey('apartments.id'))
    client_id: Mapped[not_null_int] = mapped_column(ForeignKey('clients.id'))
    check_in: Mapped[datetime.datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=False)
    check_out: Mapped[datetime.datetime]
    total_price: Mapped[not_null_int]
    status: Mapped[non_empty_str] = mapped_column(default='booked')
