from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, id_primary_key, non_empty_str, datetime_utc_timezone
from app.schemas.auth.users_auth_schemas import UsersRole
import datetime

class Users(Base):
    __tablename__ = "users"

    id: Mapped[id_primary_key]
    full_name: Mapped[non_empty_str]
    phone_number: Mapped[non_empty_str] = mapped_column(unique=True, name='phone_number')
    email: Mapped[non_empty_str] = mapped_column(unique=True, name='email')
    role: Mapped[non_empty_str] = mapped_column(default=UsersRole.CLIENT)
    hashed_password: Mapped[bytes] 
    deleted_at: Mapped[datetime_utc_timezone] = mapped_column(default=None)

    bookings: Mapped[list["Bookings"]] = relationship(back_populates="user")
