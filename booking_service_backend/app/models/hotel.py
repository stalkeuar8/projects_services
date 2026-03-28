from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, id_primary_key, non_empty_str, not_null_int, datetime_utc_timezone
import datetime

class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[id_primary_key]
    name: Mapped[non_empty_str]
    country: Mapped[non_empty_str]
    city: Mapped[non_empty_str]
    rating: Mapped[not_null_int]
    deleted_at: Mapped[datetime_utc_timezone] = mapped_column(default=None)

    rooms: Mapped[list["Rooms"]] = relationship(back_populates="hotel")


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[id_primary_key]
    hotel_id: Mapped[not_null_int] = mapped_column(ForeignKey("hotels.id", ondelete="RESTRICT", onupdate='RESTRICT'))
    category: Mapped[non_empty_str]
    capacity: Mapped[not_null_int]
    price_per_night: Mapped[not_null_int]
    deleted_at: Mapped[datetime_utc_timezone] = mapped_column(default=None)

    hotel: Mapped["Hotels"] = relationship(back_populates="rooms")
