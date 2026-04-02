from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, datetime_utc_timezone, id_primary_key, non_empty_str, not_null_int


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[id_primary_key]
    name: Mapped[non_empty_str]
    country: Mapped[non_empty_str] = mapped_column(index=True)
    city: Mapped[non_empty_str] = mapped_column(index=True)
    rating: Mapped[not_null_int] = mapped_column(index=True)
    deleted_at: Mapped[datetime_utc_timezone] = mapped_column(default=None)

    rooms: Mapped[list["Rooms"]] = relationship(back_populates="hotel")
    admin: Mapped["HotelAdmins"] = relationship(back_populates="hotel")

    __table_args__ = (
        Index("by_city_and_rating", "city", "rating"),
    )

class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[id_primary_key]
    hotel_id: Mapped[not_null_int] = mapped_column(ForeignKey("hotels.id", ondelete="RESTRICT", onupdate="RESTRICT"), index=True)
    category: Mapped[non_empty_str] = mapped_column(index=True)
    capacity: Mapped[not_null_int] 
    price_per_night: Mapped[not_null_int] = mapped_column(index=True)
    deleted_at: Mapped[datetime_utc_timezone] = mapped_column(default=None)

    hotel: Mapped["Hotels"] = relationship(back_populates="rooms")


    __table_args__ = (
        Index("by_hotel and price", "hotel_id", "price_per_night"),
    )

class HotelAdmins(Base):
    __tablename__ = "hotels_admins"

    row_id: Mapped[id_primary_key]
    hotel_id: Mapped[not_null_int] = mapped_column(ForeignKey("hotels.id", ondelete="RESTRICT", onupdate="RESTRICT"), unique=True, index=True)
    bot_hashed_password: Mapped[non_empty_str] = mapped_column(nullable=False)
    chat_id: Mapped[str] = mapped_column(unique=True, default=None, nullable=True)

    hotel: Mapped["Hotels"] = relationship(back_populates="admin")
