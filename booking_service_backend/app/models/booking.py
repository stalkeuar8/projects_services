import datetime

from sqlalchemy import DateTime, ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, datetime_utc_timezone, id_primary_key, non_empty_str, not_null_int
from app.models.hotel import Rooms


class Clients(Base):
    __tablename__ = "clients"

    id: Mapped[id_primary_key]
    full_name: Mapped[non_empty_str]
    phone_number: Mapped[non_empty_str] = mapped_column(unique=True)
    email: Mapped[non_empty_str] = mapped_column(unique=True)

    bookings: Mapped[list["Bookings"]] = relationship(back_populates="client")


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[id_primary_key]
    room_id: Mapped[not_null_int] = mapped_column(ForeignKey("rooms.id"))
    client_id: Mapped[not_null_int] = mapped_column(ForeignKey("clients.id"))
    created_at: Mapped[datetime_utc_timezone] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    check_in: Mapped[datetime_utc_timezone] = mapped_column(nullable=False)
    check_out: Mapped[datetime_utc_timezone] = mapped_column(nullable=False)
    total_price: Mapped[not_null_int]
    status: Mapped[non_empty_str] = mapped_column(default="pending")

    client: Mapped["Clients"] = relationship(back_populates="bookings")
    room: Mapped["Rooms"] = relationship()
