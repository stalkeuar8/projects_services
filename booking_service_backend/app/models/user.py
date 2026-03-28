from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, id_primary_key, non_empty_str
from app.schemas.auth.users_auth_schemas import UsersRole


class Users(Base):
    __tablename__ = "users"

    id: Mapped[id_primary_key]
    full_name: Mapped[non_empty_str]
    phone_number: Mapped[non_empty_str] = mapped_column(unique=True, name='phone_number')
    email: Mapped[non_empty_str] = mapped_column(unique=True, name='email')
    role: Mapped[non_empty_str] = mapped_column(default=UsersRole.CLIENT)
    hashed_password: Mapped[bytes] 

    bookings: Mapped[list["Bookings"]] = relationship(back_populates="user")
