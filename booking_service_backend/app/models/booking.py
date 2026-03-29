from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, datetime_utc_timezone, id_primary_key, non_empty_str, not_null_int


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[id_primary_key]
    room_id: Mapped[not_null_int] = mapped_column(ForeignKey("rooms.id", ondelete="RESTRICT", onupdate="RESTRICT"))
    user_id: Mapped[not_null_int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT", onupdate="RESTRICT"))
    created_at: Mapped[datetime_utc_timezone] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    check_in: Mapped[datetime_utc_timezone] = mapped_column(nullable=False)
    check_out: Mapped[datetime_utc_timezone] = mapped_column(nullable=False)
    total_price: Mapped[not_null_int]
    status: Mapped[non_empty_str] = mapped_column(default="pending")

    user: Mapped["Users"] = relationship(back_populates="bookings")
    room: Mapped["Rooms"] = relationship()
